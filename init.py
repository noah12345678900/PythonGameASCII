```python
import time
import os

# Function to clear the console (works on Windows, Linux, and Mac)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII art for hamburger
hamburger = """
   🍔
  /    \\
 /______\\
 |  🍔  |  Hamburger: Juicy beef patty, fresh lettuce, tomato, and bun!
 |_______|
"""

# ASCII art for hotdog
hotdog = """
   🌭
  /    \\
 /______\\
 |  🌭  |  Hotdog: Grilled sausage in a soft bun with mustard!
 |_______|
"""

# ASCII art for pizza
pizza = """
   🍕
  /    \\
 /______\\
 |  🍕  |  Pizza: Cheesy, tomato-sauced delight with a crispy crust!
 |_______|
"""

# Function to display the video sequence
def play_food_video():
    scenes = [
        ("Let's make a delicious hamburger!", hamburger, 2),
        ("Grilling the patty and assembling the bun...", hamburger, 2),
        ("Now for a classic hotdog!", hotdog, 2),
        ("Sizzling sausage with a mustard drizzle!", hotdog, 2),
        ("Time for a cheesy pizza!", pizza, 2),
        ("Baking the crust with toppings galore!", pizza, 2),
        ("All done! Which is your favorite?", hamburger + hotdog + pizza, 3)
    ]
    
    for message, art, delay in scenes:
        clear_screen()
        print(message)
        print(art)
        time.sleep(delay)

# Run the video
print("Starting the Hamburger, Hotdog, and Pizza Show!")
time.sleep(1)
play_food_video()
print("Video ended. Try running it again!")

```
