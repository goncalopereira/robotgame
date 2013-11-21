import rg

class Robot:

  def bots_close(self,location,bots,ignores):
    close = rg.locs_around(location)
    return filter(lambda t: t[0] in close and t[0] not in ignores,bots) 

  def lists(self,location,friends,enemies):
    
    close_enemies = self.bots_close(location,enemies,[])
    close_friends = self.bots_close(location,friends,[])

    enemies_step_away = []
    friends_step_away = []

    for l in rg.locs_around(location):
      e = self.bots_close(l,enemies,[location])
      map(lambda t: enemies_step_away.append(t),e)
      f = self.bots_close(l,friends,[location])
      map(lambda t: enemies_step_away.append(t),f)

    return (close_enemies,close_friends,enemies_step_away,friends_step_away)

  def score_move(self,lists):
    if len(lists[1]) > 1:
      return 0

    return len(lists[3])-len(lists[2])

  def act(self,game):
        all_friends = filter(lambda t: t[1].player_id == self.player_id and t[0] != self.location,game['robots'].items())
        all_enemies = filter(lambda t: t[1].player_id != self.player_id,game['robots'].items())        

#        current_list = self.lists(self.location,all_friends,all_enemies)

        other_lists = map(lambda l: (l,self.lists(l,all_friends,all_enemies)),
            rg.locs_around(self.location,filter_out=('invalid','spawn','obstacle'))
        )
            
        scores = map(lambda t: (self.score_move(t[1]),t[0]),other_lists)

        s = sorted(scores, reverse=True)

        return ['move',s[0][1]]

