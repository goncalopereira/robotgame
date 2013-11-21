import rg

class Robot:
      def act(self, game):

                  minDist = 1000000
                  minDistLoc = self.location
                  for loc, bot in game['robots'].iteritems():                                
                                if bot.player_id != self.player_id:
                                                  if rg.dist(loc, self.location) <= 1:
                                                                        return ['attack', loc]


                                elif rg.dist(loc,self.location) < minDist:
                                        minDist = rg.dist(loc,self.location)
                                        minDistLoc = loc

                  
                  return ['move',rg.toward(self.location,loc)]
                                                                                      
