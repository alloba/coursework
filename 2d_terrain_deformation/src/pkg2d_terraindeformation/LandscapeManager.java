/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pkg2d_terraindeformation;

import java.util.LinkedList;

/**
 * This class handles anything involving shaping of maintenence of the terrain.
 * Generation, validation, modeling impacts, the whole shizbang.
 *
 * Currently the placement of terrain points is handled by mostly random
 * numbers. This would be fine, but I'm not terribly fond of how often it throws
 * out sharp changes in direction. It isn't a focus at this point. but a
 * cleverer way to do things would be much enjoyed.
 *
 *
 * @author AbramRowell & AlexBates
 */
public class LandscapeManager {

    LinkedList<TerrainPoint> terrain;
    int segmentWidth;
    int numberOfPoints; //IMPORTANT: Although the number of points is used to determine sizing,
    //It is NOT representative of the number of points that exist in the terrain list
    //This is because of the rounding error present when converting a double to an int during gen.
    //The final X position is rounded up, so there will likely be fewer points in the terrain list than
    //what it says here, in the numberOfPoints variable.
    int[] windowDimensions;

    public LandscapeManager() {
    }

    public LandscapeManager(int xSize, int ySize, int numOfPoints) {
        this.terrain = new LinkedList<>();

        this.windowDimensions = new int[2];
        this.windowDimensions[0] = xSize;
        this.windowDimensions[1] = ySize;

        this.numberOfPoints = numOfPoints;
        this.segmentWidth = xSize / numOfPoints;

    }

    public void updateTerrainInfo(int xSize, int ySize, int numOfPoints) {
        this.windowDimensions[0] = xSize;
        this.windowDimensions[1] = ySize;

        this.numberOfPoints = numOfPoints;
        this.segmentWidth = xSize / numOfPoints;
    }

    public void generateTerrain() {
        //Not to happy about the actual end result here, but the general process is fine.
        //Starting from the center left of screen, add points a fixed width apart.
        //The height of each point is currently value picked randomly, which is a distance up or down from the previous point. it leads to very jagged edges, which is lame.

        terrain.clear();
        terrain.add(new TerrainPoint(-100, windowDimensions[1] / 2));

        int pointCount = 1;

        //this loop goes off of whether or not the window size has been reached, not if it has made the recommended number of points
        while (windowDimensions[0] + 100 >= terrain.get(pointCount - 1).xCoord) {
            double elevation = terrain.get(pointCount - 1).yCoord + (Math.random() - 0.5) * 40 * Math.pow(2, -0.5);
            double width = segmentWidth + terrain.get(pointCount - 1).xCoord;
            terrain.add(new TerrainPoint((int) width + 1, (int) elevation));

            pointCount += 1;
        }

        if (pointCount % 2 != 0) {
            terrain.add(new TerrainPoint(terrain.get(pointCount - 1).xCoord + 10, terrain.get(pointCount - 1).yCoord));
        }
    }

    public void impact(int x, int y, int direction) {
        //finds the point closest to the given impact point (X coordinate-wise)
        //sends each point within a radius of 'impactSize' to the impactCalculation method, which returns the correct offset that the terrain point needs.

        int impactForce = 55 * direction;
        int impactSize = 20;

        TerrainPoint closestPoint = new TerrainPoint(0, 0);
        int closestPointIndex = 0;

        for (TerrainPoint p : terrain) {
            if (Math.abs(p.xCoord - x) < Math.abs(closestPoint.xCoord - x)) {
                closestPoint = p;
                closestPointIndex = terrain.indexOf(p);
            }
        }
        for (int i = closestPointIndex - impactSize; i < closestPointIndex + impactSize + 1; i++) {
            if (i >= 0 && i < terrain.size()) {
                if (terrain.get(i).yCoord + impactCalculation(impactForce, closestPointIndex - i) < windowDimensions[1]) {
                    terrain.get(i).yCoord += impactCalculation(impactForce, closestPointIndex - i);
                } else {
                    terrain.get(i).yCoord = windowDimensions[1];
                }
            }
        }
    }

    public int impactCalculation(int force, int distance) {
        //uses a gaussian curve to map the deformation of the terrain.
        //the way it works now deforms it an amount shaped like a bell-curve, however it does not end with that shape.
        //if there is a spike in the terrain, it will probably still be there after the deformation.
        //or, to put another way, the returned values do not resemble something like the landscape just getting scooped out in a bowl shape

        //a*exp(- ((x-b)^2) / (2c^2) )
        double a = force;    //height of curve
        double b = 0;     //offset from origin //im keeping it in just to maintain the look of the equation, really.
        double c = 5; //steepness of curve

        double x = distance;

        double positionChange = a * Math.exp(-(((x - b) * (x - b)) / (2 * c * c)));
        return (int) positionChange;
    }

    public void shiftTerrainHorizontal(int xAmount) {
        for (TerrainPoint t : terrain) {
            t.xCoord += xAmount;
        }
        //these two statements are a bit iffy, but they seem to work.
        //if a point is out of bounds (the window +/- 100), take that point, put it on the other side,
        //  and put its position as one segment length behind the orinial last in line
        if (terrain.getLast().xCoord < windowDimensions[0] + 100) {
            terrain.addLast(terrain.remove());
            terrain.getLast().xCoord = terrain.get(terrain.size() - 2).xCoord + segmentWidth;
        }
        if (terrain.getFirst().xCoord > -100) {
            terrain.addFirst(terrain.removeLast());
            terrain.getFirst().xCoord = terrain.get(1).xCoord - segmentWidth;
        }

    }

    public void shiftTerrainVertical(int yAmount) {
        for (TerrainPoint t : terrain) {
            t.yCoord += yAmount;
        }
    }

    public LinkedList<TerrainPoint> getTerrain() {
        //straight up. nothing fancy.
        return terrain;
    }

}
