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


class XMLTree():
    """Process a given XML File. Takes File location of XML as string"""

    def __init__(self, filelocation):
        self.XMLText = open(filelocation).read()
        self.process(self.XMLText, None)
        self.sanitize(self.depthfirst())

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

    def breadthfirst(self):
        nodelist = [self.root]
        nodelist = self.breadthrecurse(self.root, nodelist)
        return nodelist

    def breadthrecurse(self, node, nodelist=[]):
        for child in node.Children:
            nodelist.append(child)
        for child in node.Children:
            self.breadthrecurse(child, nodelist)

        return nodelist

    def depthfirst(self):
        nodelist = []
        return self.depthrecurse(self.root, nodelist)

    def depthrecurse(self, node, nodelist=[]):
        for child in node.Children:
            self.depthrecurse(child, nodelist)
        nodelist.append(node)
        return nodelist

    def getresponse(self, behaviorstring):
        behaviornode = None
        responselist = []
        behaviorstring = '"' + behaviorstring + '"'
        for node in self.breadthfirst():
            if node.Behavior.lower() == behaviorstring.lower():
                behaviornode = node
                break
        if behaviornode is None:
            return "Not A Valid Input"

        for node in self.depthrecurse(behaviornode):
            if node.Response.replace('"', '').replace(' ', '') != '':
                responselist.append(node)

        return random.choice(responselist).Response
