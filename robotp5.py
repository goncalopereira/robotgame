import rg

class Robot:

      def move(self,location):
        valid_locations = rg.locs_around(self.location, filter_out=('invalid', 'obstacle','spawn'))

        sorted_valid = sorted(valid_locations, key=lambda e: rg.wdist(e,location))

        if len(sorted_valid) >= 1:
          return ['move',rg.toward(self.location,sorted_valid[0])]
        else:
          return ['guard']

      def attack(self,location):
        valid_locations = rg.locs_around(self.location, filter_out=('invalid', 'obstacle','spawn'))

        if location in valid_locations:
          return ['attack',location]
        else:
          return ['guard']

      def deal_with_enemy(self,close_enemies):     
   
        sort_closest = sorted(close_enemies, key=lambda e: e[0])

        filter_next_to = filter(lambda e: rg.wdist(e[0],self.location) <= 1, sort_closest)

        if len(filter_next_to) > 2 and self.hp <= 8:
          return ['suicide']

        if len(filter_next_to) > 1: 
          sort_hp = sorted(filter_next_to, key=lambda e: e[1].hp)
          return self.attack(sort_hp[0][0])   

        filter_very_close = filter(lambda e: rg.wdist(e[0],self.location) <= 2, sort_closest)   
        if len(filter_very_close) > 1:
          sort_hp = sorted(filter_very_close, key=lambda e: e[1].hp)
          return self.attack(rg.toward(self.location,sort_hp[0][0]))  

        return self.move(sort_closest[0][0])

      def deal_with_friends(self,close_friends):

        sort_closest = sorted(close_friends, key=lambda e: e[0])

        if rg.wdist(sort_closest[0][0],self.location) <= 1:
          return ['guard']
        else: 
          return self.move(sort_closest[0][0])

      def act(self, game):

        all_friends = filter(lambda t: t[1].player_id == self.player_id and t[0] != self.location,game['robots'].items())
        all_enemies = filter(lambda t: t[1].player_id != self.player_id,game['robots'].items())        

        if len(all_enemies) >= 1:
          return self.deal_with_enemy(all_enemies)

        if len(all_friends) >= 1:
          return self.deal_with_friends(all_friends)

        return ['guard']                                                                                  
