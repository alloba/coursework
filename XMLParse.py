import random


class Node:
    """Storage for each element in the XML Tree"""

    def __init__(self, name=""):
        self.Name = name
        self.Children = []
        self.Content = ""
        self.Behavior = ""
        self.Response = ""


    def __str__(self,level=1):
        returnstring = "     " * (level-1)
        returnstring += "-" + self.Name.capitalize() + '\n'

        if len(self.Behavior) > 2:
            returnstring += ('    ' * level) + "|" + "Behavior: " + str(self.Behavior) + '\n'

        if len(self.Response) > 3:
            returnstring += ('    ' * level) + "|" + "Response: " + str(self.Response) + '\n'

        if len(self.Children) == 0:
            returnstring += ''
        else:
            returnstring += ("    " * level) +"|" + "Children:\n" + ''

        for child in self.Children:
            returnstring += ('' * level) + child.__str__(level+1)

        return returnstring


    def addchild(self, node):
        self.Children.append(node)


    def addattribute(self, attrib):
        self.Behavior.append(attrib)


    def addelement(self, element):
        self.Content += element


class XMLTree:
    """Process a given XML File. Takes File location of XML as string"""

    def __init__(self, filelocation):
        self.XMLText = open(filelocation).read()
        self.process(self.XMLText, None)
        self.sanitize(self.buildnodelist(self.root))

    def __str__(self):
        return self.root.__str__()

    def process(self, text, parent=None):
        workingNode = Node()

        previouscharacters = ""
        if parent is None:
            self.root = workingNode
            self.XMLText = self.XMLText[1:]
        else:
            parent.addchild(workingNode)

        while len(self.XMLText) != 0:
            if self.XMLText[0] is '<' and self.XMLText[1] is not '/':
                self.XMLText = self.XMLText[1:]
                self.process(self.XMLText, workingNode)

            elif self.XMLText[0] is '/' and '>' in self.XMLText:
                workingNode.Content += previouscharacters
                self.XMLText = self.XMLText[1:]
                return

            else:
                previouscharacters += self.XMLText[0]
                self.XMLText = self.XMLText[1:]

    def sanitize(self, nodelist):
        """
        This stuff really feels held together with prayers and glue, but it works.
        Puts everything where it is supposed to be based on very strict formatting guidelines
        """

        for node in nodelist:
            node.Content = node.Content.split('>')[0]  # gets rid of junk characters left over from creating the tree
            node.Name = node.Content.split(' ')[0]  # pretty much always "node".
            node.Content += " "  # The split below needs a space, but not all nodes have space. so add it... it works...
            node.Content = node.Content.split(' ', 1)[1]

            if node.Name != 'root':  # the root node is a special flower, so exclude it
                node.Behavior += node.Content.split("behavior")[1].split('response')[0].split("=")[1].strip()
                node.Response += node.Content.split("response")[1].split("=")[1]

                node.Content = ""

    def buildnodelist(self, node):
        if node == None:
            return []
        nodelist = self.buildnodelistrecurse(node, [])
        return nodelist

    def buildnodelistrecurse(self, node, nodelist):
        bnodelist=nodelist
        if node not in bnodelist:
            bnodelist.append(node)
        for child in node.Children:
            self.buildnodelistrecurse(child, bnodelist)

        return bnodelist

    def breadthfirst(self, behaviorstring):
        global breadthnode, breadthcount
        breadthnode = None
        breadthcount = 1
        return self.breadthrecurse(self.root, behaviorstring)

    def breadthrecurse(self, node, behaviorstring, foundnode=None):
        global breadthnode, breadthcount

        for child in node.Children:
            if child.Behavior.lower() == behaviorstring.lower():
                breadthnode = child

            if breadthnode is not None:
                break
            else:
                breadthcount += 1

        for child in node.Children:
            self.breadthrecurse(child, behaviorstring, breadthnode)
        return breadthnode, breadthcount

    def depthfirst(self, behaviorstring):
        global depthnode, depthcount
        depthnode = None
        depthcount = 0
        return self.depthrecurse(self.root, behaviorstring)

    def depthrecurse(self, node, behaviorstring):
        global depthnode, depthcount
        if behaviorstring.lower() == node.Behavior.lower():
            depthnode = node
        for child in node.Children:
            if depthnode is not None:
                break
            depthcount += 1
            self.depthrecurse(child, behaviorstring)
        return depthnode, depthcount

    def getresponse(self, behaviorstring):
        responselist = []
        behaviorstring = '"' + behaviorstring + '"'

        breadthnode, breadthcount = self.breadthfirst(behaviorstring)
        depthnode, depthcount = self.depthfirst(behaviorstring)

        for node in self.buildnodelist(breadthnode)[1:]:
            if node.Response.replace('"', '').replace(' ', '') != '':
                responselist.append(node.Response)
        if len(responselist) == 0:
            return "Not A Valid Input"
        else:
            return str("Response: " + random.choice(responselist) + "\n" +
                       "DepthFirst Calls: " + str(depthcount) + "\n" +
                       "BreadthFirst Calls: " + str(breadthcount))
