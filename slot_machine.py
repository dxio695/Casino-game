import curses
import time
import random


MACHINE = [
    "╔═════════════════════════════════════════╗",
    "║      *******  SLOT MACHINE  *******     ║",
    "╠═════════════════════════════════════════╣",
    "║   ┌─────┐       ┌─────┐       ┌─────┐   ║",
    "║   │  ?  │       │  ?  │       │  ?  │   ║",
    "║   └─────┘       └─────┘       └─────┘   ║",
    "╠═════════════════════════════════════════╣",
    "║    ┌────────────┐     ┌────────────┐    ║",
    "║    │    SPIN    │     │    QUIT    │    ║",
    "║    └────────────┘     └────────────┘    ║",
    "╚═════════════════════════════════════════╝",
]



# symbols = ["C", "L", "W", "D", "|", "7"]


machine_height = 11
machine_width = 43


def play_slot(stdscr):
    curses.curs_set(0)

    # instructions
    stdscr.addstr(0, 0, "INSTRUCTION")

    # enable colors
    curses.start_color()
    curses.use_default_colors()

    # set colors
    # Syntax: curses.init_pair(pair_number, foreground_color, background_color)
    curses.init_pair(1, curses.COLOR_RED, -1)      # Cherry
    curses.init_pair(2, curses.COLOR_YELLOW, -1)   # Lemon
    curses.init_pair(3, curses.COLOR_GREEN, -1)    # Watermelon
    curses.init_pair(4, curses.COLOR_CYAN, -1)     # Diamond
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)    # BAR
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_YELLOW)     # 7 Jackpot

    # store attributes in variables
    CHERRY_COLOR = curses.color_pair(1)
    LEMON_COLOR = curses.color_pair(2)
    WATERMELON_COLOR = curses.color_pair(3)
    DIAMOND_COLOR = curses.color_pair(4)
    BAR_COLOR = curses.color_pair(5)
    JACKPOT_COLOR = curses.color_pair(6) | curses.A_BOLD  # bright 7

    symbols = ["C", "L", "W", "D", "|", "7"]
    symbol_attrs = [CHERRY_COLOR, LEMON_COLOR, WATERMELON_COLOR, DIAMOND_COLOR, BAR_COLOR, JACKPOT_COLOR]


    # center machine#
    scr_h, scr_w = stdscr.getmaxyx()  #screen height, screen width

    top = (scr_h - machine_height) // 2 - 4  #first row the machine art starts to print
    left = (scr_w - machine_width) // 2 - 2  #first column the machine art starts to print

    # draw machine frame
    for i, line in enumerate(MACHINE):
        stdscr.addstr(top + i, left, line)

    # buttons
    stdscr.addstr(top + 13, left, "      SPACE = spin          Q = quit")


    # handle input
    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            break

        delay = 0.1
        if ch == ord(' '):  # spin animation

            last_reel = [None, None, None]            
            for i in range(20):
                reels = []
                for j in range(3):
                    new_sym = random.choice(symbols)
                    while new_sym == last_reel[j]:
                        new_sym = random.choice(symbols)
                    reels.append(new_sym)

                last_reel = reels[:]

                stdscr.addstr(top + 4, left + 7, reels[0], symbol_attrs[symbols.index(reels[0])])
                stdscr.addstr(top + 4, left + 21, reels[1], symbol_attrs[symbols.index(reels[1])])
                stdscr.addstr(top + 4, left + 35, reels[2], symbol_attrs[symbols.index(reels[2])])
                stdscr.refresh()
                time.sleep(delay)
                delay *= 1.1

                curses.flushinp()
        stdscr.refresh()
    

curses.wrapper(play_slot)




def slot_cutscene():
    pass






def options():
    pass








    
    














