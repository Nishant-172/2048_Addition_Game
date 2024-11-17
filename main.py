import tkinter as tk  # Tkinter module ko import karte hain, jo GUI (graphical user interface) banane ke kaam aata hai
import random  # Random module ko import karte hain, ye tiles ko randomly add karne ke kaam aayega

# Class banate hain 2048 game ke liye
class Game2048:
    # Constructor method __init__ define karte hain, jo game setup karega
    def __init__(self, master):
        self.master = master  # Tkinter ka main window ko set karte hain
        self.master.title("2048")  # Window ka title set karte hain
        self.master.geometry("400x400")  # Window ki size set karte hain
        self.master.bind("<Key>", self.handle_key)  # Keyboard ke keys detect karne ke liye bind karte hain

        # Game ke grid size aur score ki starting values set karte hain
        self.grid_size = 4  # Grid ka size set karte hain 4x4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]  # Grid banate hain jisme 4x4 cells hain, sabke value 0 hai
        self.score = 0  # Initial score 0 rakhta hain

        self.init_grid()  # Grid ko initialize karte hain, jo tkinter labels create karega
        self.add_tile()  # Ek nayi tile add karte hain
        self.update_grid()  # Grid ko update karte hain display ke liye

    # Grid aur labels banane ka method
    def init_grid(self):
        self.tiles = []  # Empty list banate hain jisme har row ke labels store honge
        for i in range(self.grid_size):  # Har row ke liye loop chalaate hain
            row = []  # Row list banate hain
            for j in range(self.grid_size):  # Har column ke liye loop chalaate hain
                # Ek tile label banate hain, jo cell mein number dikhayega
                tile = tk.Label(self.master, text="", font=("Helvetica", 32), width=4, height=2, relief="raised")
                tile.grid(row=i, column=j, padx=5, pady=5)  # Tile ko grid mein row aur column mein place karte hain
                row.append(tile)  # Tile ko row list mein add karte hain
            self.tiles.append(row)  # Row list ko tiles list mein add karte hain

    # Nayi tile add karne ka method, jo randomly cell select karta hai
    def add_tile(self):
        # Empty cells ki list banate hain jisme abhi koi tile nahi hai
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:  # Agar empty cells available hain
            i, j = random.choice(empty_cells)  # Randomly ek cell select karte hain
            self.grid[i][j] = 2 if random.random() < 0.9 else 4  # 90% chance se '2' aur 10% chance se '4' set karte hain

    # Grid ko update aur display karne ka method
    def update_grid(self):
        for i in range(self.grid_size):  # Har row mein loop chalaate hain
            for j in range(self.grid_size):  # Har column mein loop chalaate hain
                value = self.grid[i][j]  # Current cell ka value nikalte hain
                if value == 0:  # Agar value 0 hai, toh cell ko blank display karte hain
                    self.tiles[i][j].configure(text="", bg="lightgray")  # Background color lightgray set karte hain
                else:  # Agar cell mein value hai
                    self.tiles[i][j].configure(text=str(value), bg="lightblue")  # Value aur background color lightblue set karte hain
        self.master.update_idletasks()  # Tkinter window ko refresh karte hain

    # Keyboard ke key ko detect aur handle karne ka method
    def handle_key(self, event):
        # Arrow keys check karte hain aur direction ke hisaab se move karte hain
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.move_tiles(event.keysym)  # Move tiles function call karte hain
            self.add_tile()  # Ek nayi tile add karte hain move ke baad
            self.update_grid()  # Grid ko update karte hain
            if self.check_game_over():  # Check karte hain agar game over ho gaya hai
                print("Game Over! Score:", self.score)  # Game over aur score print karte hain

    # Tiles ko move aur merge karne ka method, direction ke hisaab se
    def move_tiles(self, direction):
        if direction == 'Up':  # Agar 'Up' direction hai
            self.grid = self.transpose(self.grid)  # Grid ko transpose karte hain (column ko row bana kar)
            self.grid = self.merge_tiles(self.grid)  # Grid mein tiles ko merge karte hain
            self.grid = self.transpose(self.grid)  # Dobara transpose karke original position mein le aate hain
        elif direction == 'Down':  # Agar 'Down' direction hai
            self.grid = self.reverse(self.transpose(self.grid))  # Transpose aur reverse karte hain
            self.grid = self.merge_tiles(self.grid)  # Grid mein tiles ko merge karte hain
            self.grid = self.transpose(self.reverse(self.grid))  # Dobara reverse aur transpose karte hain
        elif direction == 'Left':  # Agar 'Left' direction hai
            self.grid = self.merge_tiles(self.grid)  # Grid mein tiles ko merge karte hain
        elif direction == 'Right':  # Agar 'Right' direction hai
            self.grid = self.reverse(self.grid)  # Grid ko reverse karte hain
            self.grid = self.merge_tiles(self.grid)  # Grid mein tiles ko merge karte hain
            self.grid = self.reverse(self.grid)  # Grid ko dobara reverse karke original position mein laate hain

    # Tiles ko merge karne ka method
    def merge_tiles(self, grid):
        score = 0  # Temporary score variable banate hain
        for i in range(self.grid_size):  # Har row ke liye loop chalaate hain
            j = 0  # Column index shuru se
            while j < self.grid_size - 1:  # Last se pehle tak loop chalaate hain
                if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:  # Agar adjacent tiles same hain
                    grid[i][j] *= 2  # Tiles ko merge karke value double karte hain
                    score += grid[i][j]  # Score mein add karte hain
                    grid[i][j+1] = 0  # Dusri tile ko zero karte hain
                    j += 2  # Next tile ke liye index update karte hain
                else:
                    j += 1  # Agar merge nahi hota toh agle tile pe chalte hain
        self.score += score  # Total score mein add karte hain
        return grid  # Updated grid return karte hain

    # Game over check karne ka method
    def check_game_over(self):
        for i in range(self.grid_size):  # Har row mein loop chalaate hain
            for j in range(self.grid_size):  # Har column mein loop chalaate hain
                if self.grid[i][j] == 0:  # Agar koi cell empty hai, toh game over nahi hai
                    return False  # Game over false return karte hain
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j+1]:  # Agar adjacent horizontal tiles same hain
                    return False  # Game over false return karte hain
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i+1][j]:  # Agar adjacent vertical tiles same hain
                    return False  # Game over false return karte hain
        return True  # Agar sab check fail ho gaye toh game over true return karte hain

    # Matrix ko transpose karne ka static method
    @staticmethod
    def transpose(matrix):
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]  # Matrix ke rows ko columns banate hain

    # Matrix ko reverse karne ka static method
    @staticmethod
    def reverse(matrix):
        return [row[::-1] for row in matrix]  # Har row ko reverse karte hain

# Main function jo program start karta hai
def main():
    root = tk.Tk()  # Tkinter ka main window banate hain
    game = Game2048(root)  # Game2048 ka object banate hain
    root.mainloop()  # Tkinter ka main loop chalaate hain

# Agar ye file directly run ho rahi hai toh main function call karte hain
if __name__ == "__main__":
    main()
