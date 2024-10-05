import numpy as np

# Zmienna globalna opisująca liczbę dziur przypadających jednemu graczowi
N_HOLES = 6

# Zmienna globalna określająca ile kamyków znajduje się w jednej dziurze na początku
N_STONES = 4

            
class Game:
    def __init__(self, discount_factor = 1.0):
        self.first_player_holes = [N_STONES] * N_HOLES + [0]
        self.second_player_holes = [N_STONES] * N_HOLES + [0]
        self.player = 0
        self.actions = [0, 1, 2, 3, 4, 5]
        self.discount_factor = discount_factor
    
    def terminal(self):
        return self.is_finished() or self.first_player_holes[-1] > 24 or self.second_player_holes[-1] > 24
    
    # Metoda sprawdzająca, czy gra jest zakończona  
    # Jeśli gra została skończona, opróżniamy planszę z kul według zasad
    def is_finished(self) -> bool:
        if sum(self.first_player_holes[:N_HOLES]) == 0:
            for i in range(N_HOLES+1):
                self.second_player_holes[-1] += self.second_player_holes[i]
                self.second_player_holes[i] = 0
            return True
        elif sum(self.second_player_holes[:N_HOLES]) == 0:
            for i in range(N_HOLES+1):
                self.first_player_holes[-1] += self.first_player_holes[i]
                self.first_player_holes[i] = 0
            return True
        else:
            return False
 
    def init_state(self):
        self.reset()
        return self.state()   
    
    def sim_transition(self, a):
        reward = self.reward_fn()
        if a != None:
            self.player = self.move(self.player, a+1)
            return (reward, self.state())
        return (reward, self.init_state())  
        
    def play_ai(self, ai_policy) -> None:
        self.reset()
        self.player = 0
        
        # Dopóki gra nie jest zakończona
        while not self.terminal():
            self.print_board()
            if self.player == 0:
                print(f"Ruch gracza {self.player+1}")
                hole_n = int(input("Wybierz numer dziury: "))
            else:
                print(f"Ruch gracza AI")
                hole_n = ai_policy(self.state())+1
                
            self.player = self.move(self.player, hole_n)
            
        self.print_board()
        # Zwracamy informacje o wygranej
        if self.first_player_holes[-1] > self.second_player_holes[-1]:
            print("\n\nZwyciężył gracz nr 1!")
        elif self.first_player_holes[-1] < self.second_player_holes[-1]:
            print("\n\nZwyciężył AI")
        else:
            print("\n\nRemis!")
            
    def play_agents(self, policy_1, policy_2, iters=1000):
        won_1 = 0
        won_2 = 0
        draws = 0
        
        for i in range(2):
            if i == 0:
                p_1 = policy_1
                p_2 = policy_2
            else:
                p_1 = policy_2
                p_2 = policy_1
            for _ in range(iters//2):
                self.reset()
                while not self.terminal():
                    if self.player == 0:
                        hole_n = p_1(self.state())+1
                    else:
                        hole_n = p_2(self.state())+1
                    self.player = self.move(self.player, hole_n)
                if self.first_player_holes[-1] == self.second_player_holes[-1]:
                    draws += 1
                elif self.first_player_holes[-1] > self.second_player_holes[-1] and i == 0:
                    won_1 += 1
                elif self.first_player_holes[-1] < self.second_player_holes[-1] and i == 1:
                    won_1 += 1
                else:
                    won_2 += 1
        print("\n\n")
        print("Agent nr1, zwycięstw: {}".format(won_1))
        print("Agent nr2, zwycięstw: {}".format(won_2))
        print("Remisów: {}".format(draws))
        print("\n\n")
                    
        
    # Metoda tworząca rozgrywkę w konsoli
    def play(self) -> None:
        player = 0
        
        # Dopóki gra nie jest zakończona
        while not self.terminal():
            self.print_board()
            print("\n\n")
            print(f"Ruch gracza {player+1}")
            hole_n = int(input("Wybierz numer dziury: "))
            player = self.move(player, hole_n)
            
        self.print_board()
        # Zwracamy informacje o wygranej
        if self.first_player_holes[-1] > self.second_player_holes[-1]:
            print("\n\nZwyciężył gracz nr 1!")
        elif self.first_player_holes[-1] < self.second_player_holes[-1]:
            print("\n\nZwyciężył gracz nr 2!")
        else:
            print("\n\nRemis!")
    
    # Metoda odpowiadająca za wykonanie ruchu
    # Zwraca informację o tym, kto wykonuje kolejny ruch
    def move(self, player: int, hole_n: int) -> int:
        # Ustalamy, które dziury są nasze, a które przeciwnika
        our_holes = self.first_player_holes if player == 0 else self.second_player_holes
        opponent_holes = self.second_player_holes if player == 0 else self.first_player_holes
        # Kontrolujemy ostatnią dziurę, do której wrzuciliśmy kulę 
        last = False
        # Indeks wybranej dziury
        idx = hole_n - 1
        previous_h_n = our_holes[idx] 
        our_holes[idx] = 0 
        
        # Proces wykonywania ruchu
        i = idx+1
        for _ in range(previous_h_n):
            # Jeśli dotarliśmy do domku przeciwnika, indeksujemy od początku
            if i == 2*N_HOLES + 1:
                i = 0
                
            # Jeśli kulka spada po naszej stronie
            if i // (N_HOLES + 1) == 0:
                our_holes[i] += 1  
            # Jeśli kulka spada po stronie przeciwnika
            else:
                opponent_holes[i % (N_HOLES + 1)] += 1
            
            # Jeśli kulka spadła do naszego domku
            if i == N_HOLES:
                last = True
            else:
                last = False
            
            # Przechodzimy do kolejnej dziury    
            i += 1
              
        # Jeśli ostatni kamień spadł do domku, mamy kolejny ruch
        if last is True:
            return player
        # Jeśli nie, to sprawdzamy czy doszło do przejęcia kulek przeciwnika
        elif i - 1 < N_HOLES and our_holes[i-1] == 1 and opponent_holes[N_HOLES-i] != 0:
            our_holes[-1] += 1 + opponent_holes[N_HOLES-i]
            our_holes[i-1] = 0
            opponent_holes[N_HOLES-i] = 0
        return int(not player)
    
    # Zwraca stan planszy w formie listy 
    def state(self) -> np.ndarray:
        fp_holes = self.first_player_holes[:-1]
        sp_holes = self.second_player_holes[:-1]
        
        if self.player == 0:
            sp_holes = sp_holes[::-1]
            return np.array([[sp_holes, fp_holes]])
        else:
            fp_holes = fp_holes[::-1]
            return np.array([[fp_holes, sp_holes]])
    
    # Resetuje grę
    def reset(self) -> None:        
        self.first_player_holes = [N_STONES] * N_HOLES + [0]
        self.second_player_holes = [N_STONES] * N_HOLES + [0]
       
    # Funkcja określająca nagrodę 
    def reward_fn(self) -> int:
        if not self.is_finished:
            return 0
            
        if self.first_player_holes[-1] > self.second_player_holes[-1]:
            return 1
        else:
            return -1
                
    # Metoda wizualizująca stan planszy
    def print_board(self) -> None:
        print("\n\n") 
        spare_space = "  "
        print(spare_space, end=spare_space)
        for i in range(N_HOLES-1, -1, -1):
            print(str(self.second_player_holes[i]).rjust(2), end=spare_space)    
        print()
        print(str(self.second_player_holes[-1]).rjust(2), end=spare_space)
        for i in range(N_HOLES):
            print(spare_space, end=spare_space)
        print(str(self.first_player_holes[-1]).rjust(2))
        print(spare_space, end=spare_space)
        for i in range(N_HOLES):
            print(str(self.first_player_holes[i]).rjust(2), end=spare_space) 
        print("\n\n")  
            
            
def main():
    game = Game()
    game.play()
       
if __name__ == "__main__":
    main()
        