import curses
import time
import random
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # get the base directory of the absolue path of current file slot_machine.py
csv_abs_path = os.path.join(base_dir, "payout-rate.csv")  # get the absolute path of the file payout-rate.csv

# get payout data from payout-rate.csv
with open(csv_abs_path, "r") as file:
    payout_data_list = file.readlines()

def slot_main():
    curses.wrapper(play_slot)


MACHINE = (
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
)



# symbols = ["C", "L", "W", "D", "|", "7"]


machine_height = 11
machine_width = 43


def play_slot(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

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
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(8, -1, curses.COLOR_RED)

    # store attributes in variables
    CHERRY_COLOR = curses.color_pair(1)
    LEMON_COLOR = curses.color_pair(2)
    WATERMELON_COLOR = curses.color_pair(3)
    DIAMOND_COLOR = curses.color_pair(4)
    BAR_COLOR = curses.color_pair(5)
    JACKPOT_COLOR = curses.color_pair(6) | curses.A_BOLD  # bright 7
    back_golden_color = curses.color_pair(7)
    back_red_color = curses.color_pair(8)


    symbols = ["C", "L", "W", "D", "|", "7"]
    symbol_attrs = [CHERRY_COLOR, LEMON_COLOR, WATERMELON_COLOR, DIAMOND_COLOR, BAR_COLOR, JACKPOT_COLOR]


    # SHOW INSTRUCTIONS
    stdscr.addstr(0, 0, "INSTRUCTION")
    # cherry
    stdscr.addstr(1, 0, "C", curses.color_pair(1))
    stdscr.addstr(1, 1, " = Cherry 🍒")
    # lemon
    stdscr.addstr(2, 0, "L", curses.color_pair(2))
    stdscr.addstr(2, 1, " = Lemon 🍋")
    # watermelon
    stdscr.addstr(3, 0, "W", curses.color_pair(3))
    stdscr.addstr(3, 1, " = Watermelon 🍉")
    #Diamond
    stdscr.addstr(4, 0, "D", curses.color_pair(4))
    stdscr.addstr(4, 1, " = Diamond 💎")
    # BAR
    stdscr.addstr(5, 0, "|", curses.color_pair(5))
    stdscr.addstr(5, 1, " = BAR 🟫")


    # DRAW MACHINE
    # center machine#
    scr_h, scr_w = stdscr.getmaxyx()  #screen height, screen width

    top = (scr_h - machine_height) // 2 - 4  #first row the machine art starts to print
    left = (scr_w - machine_width) // 2 - 2  #first column the machine art starts to print

    # draw machine frame
    for i, line in enumerate(MACHINE):
        stdscr.addstr(top + i, left, line)

    # buttons
    stdscr.addstr(top + 13, left, "      SPACE = spin          Q = quit")
    


    # SHOW PAYOUT DATA
    # write 777
    stdscr.addstr(0, 122, " !!! ", back_red_color)
    stdscr.addstr(0, 127, "777", JACKPOT_COLOR)
    stdscr.addstr(0, 130, "  x500 COINS", back_golden_color)
    stdscr.addstr(0, 142, " !!! ", back_red_color)
    
    # write from 77| to DDD
    for y in range(2, 8):
        payout_data_syms = payout_data_list[y].strip().split(",")[0]
        x = 127
        for ch in payout_data_syms:
            if ch == "&":
                stdscr.addstr(y, x, ch)
                x += 1
            else:
                stdscr.addstr(y, x, ch, symbol_attrs[symbols.index(ch)])
                x += 1

            payout_data_muls = payout_data_list[y].strip().split(",")[2]
            stdscr.addstr(y, x + 1, f"  x{payout_data_muls} COINS")

    # button to show all and show less
    show_all_button = (
    "┌─────────────┐",
    "│ SHOW ALL(s) │",
    "└─────────────┘",
    )

    show_less_button = (
    "┌──────────────┐",
    "│ SHOW LESS(s) │",
    "└──────────────┘",
    )


    # DRAW SHOW ALL BUTTON(SAB = show all button)
    SAB_x = 127
    SAB_i = 0
    for SAB_y in range(9, 12):
        stdscr.addstr(SAB_y, SAB_x, show_all_button[SAB_i])
        SAB_i += 1


    show_all = False


    # HANDLE INPUT
    while True:
        # quit
        ch = stdscr.getch()
        if ch == ord('q'):
            break

        # spin animation
        delay = 0.1
        if ch == ord(' '):

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


        # show all/less if 's' is pressed
        if ch == ord('s'):
            if show_all == False:
                show_all = True
                # erase current show all button
                for _SAB_Y in range(11, 8, -1):
                    stdscr.addstr(_SAB_Y, SAB_x, " " * 15)

                stdscr.refresh()
                time.sleep(0.25)

                # print all payout info
                for y in range(2, 22):
                    payout_data_syms = payout_data_list[y].strip().split(",")[0]
                    x = 127
                    for ch in payout_data_syms:
                        if ch == "&":
                            stdscr.addstr(y, x, ch)
                            x += 1
                        else:
                            stdscr.addstr(y, x, ch, symbol_attrs[symbols.index(ch)])
                            x += 1

                        payout_data_muls = payout_data_list[y].strip().split(",")[2]
                        stdscr.addstr(y, x + 1, f"  x{payout_data_muls} COINS")

                # draw show less button(SLB = show less button)
                SLB_x = 127  # also 127, same as SAB but for readibility
                SLB_i = 0
                for SLB_y in range(23, 26):
                    stdscr.addstr(SLB_y, SLB_x, show_less_button[SLB_i])
                    SLB_i += 1
                        

            elif show_all == True:
                show_all = False
                # erase current show less button
                for _SLB_Y in range(25, 22, -1):
                    stdscr.addstr(_SLB_Y, SLB_x, " " * 16)

                # erase abundant info
                for y in range(8, 22):
                    stdscr.addstr(y, 127, " " * 19)

                # draw show all button again
                SAB_x = 127
                SAB_i = 0
                for SAB_y in range(9, 12):
                    stdscr.addstr(SAB_y, SAB_x, show_all_button[SAB_i])
                    SAB_i += 1

            curses.flushinp()


        stdscr.refresh()
        time.sleep(0.05)

        





def slot_cutscene():
    pass






def options():
    pass







slot_main()