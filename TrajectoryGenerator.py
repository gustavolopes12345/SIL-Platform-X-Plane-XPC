import math

class TrajectoryGenerator:
    @staticmethod
    def nextWaypoint(currentPosition, currentTargetWaypoint, target_waypoint_array, currentWaypointInArray):
        '''Trajectory generator module'''
        distanceToWaypoint = TrajectoryGenerator.haversine(currentPosition, currentTargetWaypoint)

        if distanceToWaypoint <= 500:  # 500 meters
            currentWaypointInArray += 1
            if currentWaypointInArray == len(target_waypoint_array):
                currentWaypointInArray = 0
            currentTargetWaypoint = target_waypoint_array[currentWaypointInArray]

        return currentTargetWaypoint, currentWaypointInArray

    @staticmethod
    def haversine(coord1, coord2):
        '''Calculates the distance between two points on a sphere from their latitudes and longitude'''
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    @staticmethod
    def calculates_LOS(currentPosition, waypointPosition):
        '''Calculates the LOS (line-of-sight) angle between the current position and the waypoint'''
        lat1 = math.radians(currentPosition[0])
        lat2 = math.radians(waypointPosition[0])

        diffLong = math.radians(waypointPosition[1] - currentPosition[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                               * math.cos(lat2) * math.cos(diffLong))

        initialLOS = math.atan2(x, y)
        initialLOS = math.degrees(initialLOS)
        LOS = (initialLOS + 360) % 360

        return LOS
