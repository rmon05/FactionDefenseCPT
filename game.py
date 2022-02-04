# pygame template
import pygame
import random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_BACKSPACE, K_1, K_2, K_3

#Initialize
pygame.init()
#Set screen dimensions
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
#Create screen
screen = pygame.display.set_mode(SIZE)
#Create clock
clock = pygame.time.Clock()
#Name the program
pygame.display.set_caption("Faction Defence")

# ---------------------------
# Fonts
menu_font = pygame.font.SysFont("Georgia", 25, True, False)
health_font = pygame.font.SysFont("Georgia", 14, True, False)
game_font = pygame.font.SysFont("Georgia", 14, False, False)
faction_name_font = pygame.font.SysFont("Georgia", 32, True, False)
game_title_font = pygame.font.SysFont("Georgia", 96, True, False)

# Colours
DEFAULT = (49, 51, 53)
current_faction_colour = (-1, -1, -1)

# Buttons
#General
play_button = pygame.Rect(400, 700, 200, 100) # (MIDDLE)
view_back_button = pygame.Rect(300, 645, 100, 50) # (ON THE FACTION SELECT SCREEN)

#Select Buttons
select_button_1 = pygame.Rect(300, 200, 190, 85)
select_button_2 = pygame.Rect(700, 200, 190, 85)
select_button_3 = pygame.Rect(300, 600, 190, 85)
select_button_4 = pygame.Rect(700, 600, 190, 85)

#Info/View Buttons
view_button_1 = pygame.Rect(300, 290, 190, 85)
view_button_2 = pygame.Rect(700, 290, 190, 85)
view_button_3 = pygame.Rect(300, 690, 190, 85)
view_button_4 = pygame.Rect(700, 690, 190, 85)

# ---------------------------
#Game runs while running is True
running = True
#The player's selected faction - 0 is none
faction = 0
# Level
level = 1
# Health
total_health = 10000
current_health = 10000
#XP for level
required_XP = level*1000
current_XP = 0
#Used to update the enemies (add new enemies)
outlaw_counter = 0
speedy_counter = 0
brute_counter = 0
shifter_counter = 0
chief_counter = 0
#Speed of the enemies (can be altered through abilities)
outlaw_speed = 1
speedy_speed = 5
brute_speed = 0.5
shifter_speed = 1
chief_speed = 0.5
#Cooldown Counters - 0 is on cooldown
pyro_1_cd = 0
pyro_2_cd = 0
pyro_3_cd = 0
naturo_1_cd = 0
naturo_2_cd = 0
naturo_3_cd = 0
cryo_1_cd = 0
cryo_2_cd = 0
cryo_3_cd = 0
electro_1_cd = 0
electro_2_cd = 0
electro_3_cd = 0

# ---------------------------

#Store all of the outlaws (Costs 50 hp) (Has TBD hp)
outlaws = []
# Which outlaws need to be removed
pending_removal_outlaws = []

#Store all of the speedy outlaws (Costs 50 hp) (Has TBD hp)
speedy = []
# Which speedy need to be removed
pending_removal_speedy = []

#Store all of the brutes (Costs 100 hp) (Has TBD hp)
brutes = []
# Which brutes need to be removed
pending_removal_brutes = []

#Store all of the shifters (Costs 25 hp) (Has TBD hp)
shifters = []
# Which shifters need to be removed
pending_removal_shifters = []

#Store all of the chiefs (Costs 250 hp) (Has TBD hp)
chiefs = []
# Which outlaws need to be removed
pending_removal_chiefs = []



# ---------------------------
colour_oscillator = 0
oscillation_direction = 1
#Drawing Faction Icons
def faction_1_icon(x, y):
    global colour_oscillator
    global oscillation_direction
    pygame.draw.rect(screen, (255, 0, 0), [x, y, 190, 190], 0)
    name_text = faction_name_font.render("PYRO", True, (colour_oscillator,0,0))
    screen.blit(name_text, [x + 50,y + 75])
    # Update colour
    if colour_oscillator == 0:
        oscillation_direction = 1
        colour_oscillator += 1
    elif colour_oscillator == 255:
        oscillation_direction = -1
        colour_oscillator -= 1
    else:
        colour_oscillator+=oscillation_direction
def faction_2_icon(x, y):
    global colour_oscillator
    global oscillation_direction
    pygame.draw.rect(screen, (0, 255, 0), [x, y, 190, 190], 0)
    name_text = faction_name_font.render("NATURO", True, (0, colour_oscillator, 0))
    screen.blit(name_text, [x + 20, y + 75])
    # Update colour
    if colour_oscillator == 0:
        oscillation_direction = 1
        colour_oscillator += 1
    elif colour_oscillator == 255:
        oscillation_direction = -1
        colour_oscillator -= 1
    else:
        colour_oscillator += oscillation_direction
def faction_3_icon(x, y):
    global colour_oscillator
    global oscillation_direction
    pygame.draw.rect(screen, (0, 0, 255), [x, y, 190, 190], 0)
    name_text = faction_name_font.render("CRYO", True, (0, 0, colour_oscillator))
    screen.blit(name_text, [x + 45, y + 75])
    # Update colour
    if colour_oscillator == 0:
        oscillation_direction = 1
        colour_oscillator += 1
    elif colour_oscillator == 255:
        oscillation_direction = -1
        colour_oscillator -= 1
    else:
        colour_oscillator += oscillation_direction
def faction_4_icon(x, y):
    global colour_oscillator
    global oscillation_direction
    pygame.draw.rect(screen, (255, 255, 0), [x, y, 190, 190], 0)
    name_text = faction_name_font.render("ELECTRO", True, (colour_oscillator, colour_oscillator, 0))
    screen.blit(name_text, [x + 15, y + 75])
    # Update colour
    if colour_oscillator == 0:
        oscillation_direction = 1
        colour_oscillator += 1
    elif colour_oscillator == 255:
        oscillation_direction = -1
        colour_oscillator -= 1
    else:
        colour_oscillator += oscillation_direction

# Faction 1 Info
def view_faction1():
    #Icon
    faction_1_icon(300,30)
    pygame.draw.rect(screen, (175, 0, 175), [300, 30, 190, 190], 2)
    #Faction Name
    faction_name_text = faction_name_font.render("Faction: PYRO", True, (255,0,0))
    screen.blit(faction_name_text, [300, 225])
    #Faction Description
    line_1 = game_font.render("The Pyro wield the elementary power of heat and fire", True, (0,0,0))
    line_2 = game_font.render("Strengths: High area damage and moderate sustain", True, (0,0,0))
    line_3 = game_font.render("Weaknesses: No displacement and disruption effects", True, (0,0,0))
    screen.blit(line_1, [300, 275])
    screen.blit(line_2, [300, 300])
    screen.blit(line_3, [300, 325])
    #Abilities icons
    abilities(300, 425, 0, 0, 0)
    #Abilities description
    #Basic Attack
    basic = game_font.render("Mouse clicks kill a single enemy and plunder experience", True, (0,0,0))
    screen.blit(basic, [355, 425])
    #Ability 1
    ability_1_ln1 = game_font.render("Go on a fiery rampage!!!", True, (0,0,0))
    ability_1_ln2 = game_font.render("Your next 5 basic attacks restore 100 health and reduce all cooldowns by 1 second", True, (0,0,0))
    ability_1_cd = game_font.render(f"Cooldown: 5 seconds", True, (0,0,0))
    screen.blit(ability_1_ln1, [355, 480])
    screen.blit(ability_1_ln2, [355, 494])
    screen.blit(ability_1_cd, [355, 508])
    #Ability 2
    ability_2_ln1 = game_font.render("Launch a fireball with radius 100, killing all units hit", True, (0,0,0))
    ability_2_ln2 = game_font.render("Note: Does not plunder experience", True, (0,0,0))
    ability_2_cd = game_font.render(f"Cooldown: 5 seconds", True, (0, 0, 0))
    screen.blit(ability_2_ln1, [355, 535])
    screen.blit(ability_2_ln2, [355, 549])
    screen.blit(ability_2_cd, [355, 563])
    #Ability 3
    ability_3_ln1 = game_font.render("Instantly incinerate all enemies on the battlefield", True, (0,0,0))
    ability_3_ln2 = game_font.render("Note: Does not plunder experience", True, (0,0,0))
    ability_3_cd = game_font.render(f"Cooldown: 20 seconds", True, (0, 0, 0))
    screen.blit(ability_3_ln1, [355, 590])
    screen.blit(ability_3_ln2, [355, 604])
    screen.blit(ability_3_cd, [355, 618])
# Faction 2 Info
def view_faction2():
    #Icon
    faction_2_icon(300,30)
    pygame.draw.rect(screen, (175, 0, 175), [300, 30, 190, 190], 2)
    #Faction Name
    faction_name_text = faction_name_font.render("Faction: NATURO", True, (0,255,0))
    screen.blit(faction_name_text, [300, 225])
    #Faction Description
    line_1 = game_font.render("The Naturo wield the ancient ability to harness nature and heal", True, (0,0,0))
    line_2 = game_font.render("Strengths: High sustain and moderate disruption effects", True, (0, 0, 0))
    line_3 = game_font.render("Weaknesses: No damaging effects", True, (0, 0, 0))
    screen.blit(line_1, [300, 275])
    screen.blit(line_2, [300, 300])
    screen.blit(line_3, [300, 325])
    #Abilities icons
    abilities(300, 425, 0, 0, 0)
    # Abilities description
    # Basic Attack
    basic = game_font.render("Mouse clicks kill a single enemy and plunder experience", True, (0, 0, 0))
    screen.blit(basic, [355, 425])
    # Ability 1
    ability_1_ln1 = game_font.render("Harness natural vegetation to heal for a small amount", True, (0, 0, 0))
    ability_1_ln2 = game_font.render("Instantly restore 250 health", True, (0, 0, 0))
    ability_1_cd = game_font.render(f"Cooldown: 2 seconds", True, (0, 0, 0))
    screen.blit(ability_1_ln1, [355, 480])
    screen.blit(ability_1_ln2, [355, 494])
    screen.blit(ability_1_cd, [355, 508])
    # Ability 2
    ability_2_ln1 = game_font.render("Hijack the evolutionary tree to alter the enemies' size", True, (0, 0, 0))
    ability_2_ln2 = game_font.render("All enemies are doubled in size for 3 seconds", True, (0, 0, 0))
    ability_2_cd = game_font.render(f"Cooldown: 5 seconds", True, (0, 0, 0))
    screen.blit(ability_2_ln1, [355, 535])
    screen.blit(ability_2_ln2, [355, 549])
    screen.blit(ability_2_cd, [355, 563])
    # Ability 3
    ability_3_ln1 = game_font.render("Harness the inconceivably immense power of grapes to heal for a large amount", True, (0, 0, 0))
    ability_3_ln2 = game_font.render("Instantly restore 50% of missing health", True, (0, 0, 0))
    ability_3_cd = game_font.render(f"Cooldown: 10 seconds", True, (0, 0, 0))
    screen.blit(ability_3_ln1, [355, 590])
    screen.blit(ability_3_ln2, [355, 604])
    screen.blit(ability_3_cd, [355, 618])
# Faction 3 Info
def view_faction3():
    #Icon
    faction_3_icon(300,30)
    pygame.draw.rect(screen, (175, 0, 175), [300, 30, 190, 190], 2)
    #Faction Name
    faction_name_text = faction_name_font.render("Faction: CRYO", True, (0,0,255))
    screen.blit(faction_name_text, [300, 225])
    #Faction Description
    line_1 = game_font.render("The Cryo wield the freezing weapons of water and ice", True, (0,0,0))
    line_2 = game_font.render("Strengths: High amount of disruption effects and moderate sustain", True, (0, 0, 0))
    line_3 = game_font.render("Weaknesses: No damaging effects", True, (0, 0, 0))
    screen.blit(line_1, [300, 275])
    screen.blit(line_2, [300, 300])
    screen.blit(line_3, [300, 325])
    #Abilities icons
    abilities(300, 425, 0, 0, 0)
    # Abilities description
    # Basic Attack
    basic = game_font.render("Mouse clicks kill a single enemy and plunder experience", True, (0, 0, 0))
    screen.blit(basic, [355, 425])
    # Ability 1
    ability_1_ln1 = game_font.render("Apply cryotherapy to heal a moderate amount", True, (0, 0, 0))
    ability_1_ln2 = game_font.render("Restore 1200 health over 10 seconds", True, (0, 0, 0))
    ability_1_cd = game_font.render(f"Cooldown: 15 seconds", True, (0, 0, 0))
    screen.blit(ability_1_ln1, [355, 480])
    screen.blit(ability_1_ln2, [355, 494])
    screen.blit(ability_1_cd, [355, 508])
    # Ability 2
    ability_2_ln1 = game_font.render("Create a cold gust of wind", True, (0, 0, 0))
    ability_2_ln2 = game_font.render("Slows all enemies by 75% for 4 seconds", True, (0, 0, 0))
    ability_2_cd = game_font.render(f"Cooldown: 6 seconds", True, (0, 0, 0))
    screen.blit(ability_2_ln1, [355, 535])
    screen.blit(ability_2_ln2, [355, 549])
    screen.blit(ability_2_cd, [355, 563])
    # Ability 3
    ability_3_ln1 = game_font.render("Conjure a freezing blizzard", True, (0, 0, 0))
    ability_3_ln2 = game_font.render("Freezes all enemies in place for 8 seconds", True, (0, 0, 0))
    ability_3_cd = game_font.render(f"Cooldown: 15 seconds", True, (0, 0, 0))
    screen.blit(ability_3_ln1, [355, 590])
    screen.blit(ability_3_ln2, [355, 604])
    screen.blit(ability_3_cd, [355, 618])
# Faction 4 Info
def view_faction4():
    #Icon
    faction_4_icon(300,30)
    pygame.draw.rect(screen, (175, 0, 175), [300, 30, 190, 190], 2)
    #Faction Name
    faction_name_text = faction_name_font.render("Faction: ELECTRO", True, (255,255,0))
    screen.blit(faction_name_text, [300, 225])
    #Faction Description
    line_1 = game_font.render("The Electro wield the innovative tools of light and electricity", True, (0,0,0))
    line_2 = game_font.render("Strengths: High area damage and moderate displacement effectd", True, (0, 0, 0))
    line_3 = game_font.render("Weaknesses: No sustaining effects", True, (0, 0, 0))
    screen.blit(line_1, [300, 275])
    screen.blit(line_2, [300, 300])
    screen.blit(line_3, [300, 325])
    #Abilities icons
    abilities(300, 425, 0, 0, 0)
    # Abilities description
    # Basic Attack
    basic = game_font.render("Mouse clicks kill a single enemy and plunder experience", True, (0, 0, 0))
    screen.blit(basic, [355, 425])
    # Ability 1
    ability_1_ln1 = game_font.render("Warp space-time to concentrate all enemies on target location", True, (0, 0, 0))
    ability_1_ln2 = game_font.render("Note: No damage is dealt to any enemies", True, (0, 0, 0))
    ability_1_cd = game_font.render(f"Cooldown: 10 seconds", True, (0, 0, 0))
    screen.blit(ability_1_ln1, [355, 480])
    screen.blit(ability_1_ln2, [355, 494])
    screen.blit(ability_1_cd, [355, 508])
    # Ability 2
    ability_2_ln1 = game_font.render("Launch an electric ray in a line, killing all units whose centre is hit", True, (0, 0, 0))
    ability_2_ln2 = game_font.render("Note: Does not plunder experience", True, (0, 0, 0))
    ability_2_cd = game_font.render(f"Cooldown: 8 seconds", True, (0, 0, 0))
    screen.blit(ability_2_ln1, [355, 535])
    screen.blit(ability_2_ln2, [355, 549])
    screen.blit(ability_2_cd, [355, 563])
    # Ability 3
    ability_3_ln1 = game_font.render("Create a circular zap field which follows the cursor for 7 seconds, killing all units hit", True, (0, 0, 0))
    ability_3_ln2 = game_font.render("Note: Does not plunder experience", True, (0, 0, 0))
    ability_3_cd = game_font.render(f"Cooldown: 30 seconds", True, (0, 0, 0))
    screen.blit(ability_3_ln1, [355, 590])
    screen.blit(ability_3_ln2, [355, 604])
    screen.blit(ability_3_cd, [355, 618])

#Display Faction select
def faction_select():
    # Faction Select Grid 2x2
    pygame.draw.line(screen, (0, 0, 0), [600, 0], [600, 800], 1)
    pygame.draw.line(screen, (0, 0, 0), [200, 400], [1000, 400], 1)
    # Faction 1 Display
    faction_1_icon(300, 5)
    pygame.draw.rect(screen, (0, 0, 0), select_button_1, 0)
    select_text_1 = menu_font.render("Select", True, (255, 255, 255))
    screen.blit(select_text_1, [355, 225])
    pygame.draw.rect(screen, (0, 0, 0), view_button_1, 0)
    view_text_1 = menu_font.render("View", True, (255, 255, 255))
    screen.blit(view_text_1, [360, 315])
    # Faction 2 Display
    faction_2_icon(700, 5)
    pygame.draw.rect(screen, (0, 0, 0), select_button_2, 0)
    select_text_2 = menu_font.render("Select", True, (255, 255, 255))
    screen.blit(select_text_2, [755, 225])
    pygame.draw.rect(screen, (0, 0, 0), view_button_2, 0)
    view_text_2 = menu_font.render("View", True, (255, 255, 255))
    screen.blit(view_text_2, [760, 315])
    # Faction 3 Display
    faction_3_icon(300, 405)
    pygame.draw.rect(screen, (0, 0, 0), select_button_3, 0)
    select_text_3 = menu_font.render("Select", True, (255, 255, 255))
    screen.blit(select_text_3, [355, 625])
    pygame.draw.rect(screen, (0, 0, 0), view_button_3, 0)
    view_text_3 = menu_font.render("View", True, (255, 255, 255))
    screen.blit(view_text_3, [360, 715])
    # Faction 4 Display
    faction_4_icon(700, 405)
    pygame.draw.rect(screen, (0, 0, 0), select_button_4, 0)
    select_text_4 = menu_font.render("Select", True, (255, 255, 255))
    screen.blit(select_text_4, [755, 625])
    pygame.draw.rect(screen, (0, 0, 0), view_button_4, 0)
    view_text_4 = menu_font.render("View", True, (255, 255, 255))
    screen.blit(view_text_4, [760, 715])

#Display Ability List
def abilities(x, y, r, g, b):
    # Basic Attack (Click)
    pygame.draw.rect(screen, (r, g, b), [x, y, 50, 50], 0)
    passive_text = game_font.render("B", True, (255-r, 255-g, 255-b))
    screen.blit(passive_text, [x + 2, y])
    # Ability 1 icon
    pygame.draw.rect(screen, (r, g, b), [x, y+55, 50, 50], 0)
    a1_text = game_font.render("1", True, (255 - r, 255 - g, 255 - b))
    screen.blit(a1_text, [x + 2, y + 55])
    # Ability 2 icon
    pygame.draw.rect(screen, (r, g, b), [x, y+110, 50, 50], 0)
    a2_text = game_font.render("2", True, (255 - r, 255 - g, 255 - b))
    screen.blit(a2_text, [x + 2, y + 110])
    # Ultimate Ability icon
    pygame.draw.rect(screen, (r, g, b), [x, y+165, 50, 50], 0)
    ult_text = game_font.render("3", True, (255 - r, 255 - g, 255 - b))
    screen.blit(ult_text, [x + 2, y + 165])

    # Ability CD display
    if faction == 1:
        a_1_cd_text = game_font.render(str(round(pyro_1_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_2_cd_text = game_font.render(str(round(pyro_2_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_3_cd_text = game_font.render(str(round(pyro_3_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        screen.blit(a_1_cd_text, [x + 2, y + 75])
        screen.blit(a_2_cd_text, [x + 2, y + 130])
        screen.blit(a_3_cd_text, [x + 2, y + 185])
    elif faction == 2:
        a_1_cd_text = game_font.render(str(round(naturo_1_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_2_cd_text = game_font.render(str(round(naturo_2_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_3_cd_text = game_font.render(str(round(naturo_3_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        screen.blit(a_1_cd_text, [x + 2, y + 75])
        screen.blit(a_2_cd_text, [x + 2, y + 130])
        screen.blit(a_3_cd_text, [x + 2, y + 185])
    elif faction == 3:
        a_1_cd_text = game_font.render(str(round(cryo_1_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_2_cd_text = game_font.render(str(round(cryo_2_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_3_cd_text = game_font.render(str(round(cryo_3_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        screen.blit(a_1_cd_text, [x + 2, y + 75])
        screen.blit(a_2_cd_text, [x + 2, y + 130])
        screen.blit(a_3_cd_text, [x + 2, y + 185])
    elif faction == 4:
        a_1_cd_text = game_font.render(str(round(electro_1_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_2_cd_text = game_font.render(str(round(electro_2_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        a_3_cd_text = game_font.render(str(round(electro_3_cd / 60, 2)), True, (255 - r, 255 - g, 255 - b))
        screen.blit(a_1_cd_text, [x + 2, y + 75])
        screen.blit(a_2_cd_text, [x + 2, y + 130])
        screen.blit(a_3_cd_text, [x + 2, y + 185])

#Display Left HUD
def left_hud(r,g,b):
    global current_health
    global total_health
    # LEFT BOARD
    pygame.draw.rect(screen, (0, 0, 0), [0, 0, 200, 800], 0)
    # Health Bar
    pygame.draw.rect(screen, (175, 0, 0), [5, 5, 190, 20], 0)
    pygame.draw.rect(screen, (34, 139, 34), [5, 5, 190 * (current_health / total_health), 20], 0)
    health_text = health_font.render(f"{current_health}/{total_health}", True, (0, 0, 0))
    screen.blit(health_text, [60, 5])
    # Faction Icon + Border
    pygame.draw.rect(screen, (r, g, b), [5, 30, 190, 190], 0)
    pygame.draw.rect(screen, (175, 0, 175), [5, 30, 190, 190], 2)
    # Display Abilities
    abilities(5, 225, 255, 255, 255)
    # Display Enemies
    enemies_info()

#Display Level
def level_display():
    global required_XP
    global current_XP
    global level
    #Level Bar (XP)
    pygame.draw.rect(screen, (211, 211, 211), [5, 500, 190, 20], 0)
    pygame.draw.rect(screen, (0, 204, 255), [5, 500, 190*(current_XP/required_XP), 20], 0)
    #Experience Text (XP)
    xp_text = health_font.render(f"{current_XP}/{required_XP}", True, (0, 0, 0))
    screen.blit(xp_text, [60, 500])
    #Level Text
    level_text = health_font.render(f"Level {level}", True, (255, 255, 255))
    screen.blit(level_text, [60, 475])

#Display the information relating to the enemies
def enemies_info():
    #Outlaw
    pygame.draw.circle(screen, (255, 255, 255), [30,550], 10)
    outlaw_text = health_font.render("Deals 100 Damage", True, (255, 255, 255))
    screen.blit(outlaw_text, [57, 540])
    #Speedy
    pygame.draw.circle(screen, (150, 150, 150), [30,575], 10)
    speedy_text = health_font.render("Deals 500 Damage", True, (255, 255, 255))
    screen.blit(speedy_text, [57, 565])
    #Brute
    pygame.draw.circle(screen, (150, 0, 0), [30,625], 25)
    brute_text = health_font.render("Deals 1000 Damage", True, (255, 255, 255))
    screen.blit(brute_text, [57, 615])
    #Shifter
    temp_shifter_colour = random.randint(0, 255)
    pygame.draw.circle(screen, (temp_shifter_colour, temp_shifter_colour, temp_shifter_colour), [30,675], 15)
    shifter_text_1 = health_font.render("Deals 500 Damage", True, (255, 255, 255))
    shifter_text_2 = health_font.render("Shifts Colour", True, (255, 255, 255))
    screen.blit(shifter_text_1, [57, 660])
    screen.blit(shifter_text_2, [57, 675])
    #Chief
    pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),[5, 700, 50, 50], 0)
    chief_text_1 = health_font.render("Deals 2500 Damage", True, (255, 255, 255))
    chief_text_2 = health_font.render("Spawns Enemies", True, (255, 255, 255))
    screen.blit(chief_text_1, [57, 710])
    screen.blit(chief_text_2, [57, 725])
    #Win condition
    wincon_text = health_font.render("Complete Level 10 to Win!", True, (255, 255, 255))
    screen.blit(wincon_text, [5, 765])


# ---------------------------
#Pyro Abilities
#Healing Attacks Counter - 0 means none left
healing_attacks = 0
def pyro_1():
    global pyro_1_cd
    if pyro_1_cd == 0:
        global healing_attacks
        healing_attacks = 5
        #Update cooldown
        pyro_1_cd = 300

#Animating the circle
circle_time = 0
circle_x = -1
circle_y = -1
def pyro_2(x,y):
    global circle_time
    global pyro_2_cd
    global circle_x
    global circle_y
    if pyro_2_cd == 0:
        circle_time = 20
        #For displaying the explosion circle
        circle_x = x
        circle_y = y
        aoe_circle = pygame.draw.circle(screen, (255, 125, 0), [x,y], 100)
        for i in range(len(outlaws)):
            aoe_hit = aoe_circle.collidepoint(outlaws[i])
            if aoe_hit == 1:
                pending_removal_outlaws.append((outlaws[i][0]-outlaw_speed, outlaws[i][1]))
        for i in range(len(speedy)):
            aoe_hit = aoe_circle.collidepoint(speedy[i])
            if aoe_hit == 1:
                pending_removal_speedy.append((speedy[i][0]-speedy_speed, speedy[i][1]))
        for i in range(len(brutes)):
            aoe_hit = aoe_circle.collidepoint(brutes[i])
            if aoe_hit == 1:
                pending_removal_brutes.append((brutes[i][0]-brute_speed, brutes[i][1]))
        for i in range(len(shifters)):
            aoe_hit = aoe_circle.collidepoint(shifters[i])
            if aoe_hit == 1:
                pending_removal_shifters.append((shifters[i][0]-shifter_speed, shifters[i][1]))
        for i in range(len(chiefs)):
            aoe_hit = aoe_circle.collidepoint(chiefs[i])
            if aoe_hit == 1:
                pending_removal_chiefs.append((chiefs[i][0]-chief_speed, chiefs[i][1]))
        # Update cooldown
        pyro_2_cd = 300

def pyro_ult():
    global pyro_3_cd
    if pyro_3_cd == 0:
        #Wipes the whole board
        outlaws.clear()
        speedy.clear()
        brutes.clear()
        shifters.clear()
        chiefs.clear()
        pyro_3_cd = 1200


#Naturo Abilities
def naturo_1():
    global current_health
    global total_health
    global naturo_1_cd
    if naturo_1_cd == 0:
        amount_healed = 250
        if current_health+amount_healed>=total_health:
            current_health = total_health
        else:
            current_health += amount_healed
        # Update cooldown
        naturo_1_cd = 120

#Time under polymorph
polymorph_time_counter = 0
def naturo_2():
    global polymorph_time_counter
    global naturo_2_cd
    if naturo_2_cd == 0:
        polymorph_time_counter = 180
        # Update cooldown
        naturo_2_cd = 300

def naturo_ult():
    global current_health
    global total_health
    global naturo_3_cd
    if naturo_3_cd == 0:
        amount_healed = int(0.5*(total_health-current_health))
        current_health+=amount_healed
        # Update cooldown
        naturo_3_cd = 600


#Cryo Abilities
#Healing time
cryo_time = 0
def cryo_1():
    global cryo_time
    global cryo_1_cd
    if cryo_1_cd == 0:
        cryo_time = 600
        # Update cooldown
        cryo_1_cd = 900

#Slow time
slow_time = 0
def cryo_2():
    global slow_time
    global cryo_2_cd
    if cryo_2_cd == 0:
        slow_time = 240
        # Update cooldown
        cryo_2_cd = 360
#Freeze time
freeze_time = 0
def cryo_ult():
    global freeze_time
    global cryo_3_cd
    if cryo_3_cd == 0:
        freeze_time = 480
        # Update cooldown
        cryo_3_cd = 900

#Electro Abilities
def electro_1(x, y):
    global electro_1_cd
    if electro_1_cd == 0:
        for i in range(len(outlaws)):
            outlaws[i] = (x, y)
        for i in range(len(speedy)):
            speedy[i] = (x, y)
        for i in range(len(brutes)):
            brutes[i] = (x, y)
        for i in range(len(shifters)):
            shifters[i] = (x, y)
        for i in range(len(chiefs)):
            chiefs[i] = (x, y)

        # Update cooldown
        electro_1_cd = 600

#Animating the Line
line_time = 0
line_y = -1
def electro_2(y):
    global line_time
    global line_y
    global electro_2_cd
    if electro_2_cd == 0:
        line_time = 20
        aoe_line = pygame.draw.rect(screen, (255, 255, 0), [200, y-8, 800, 16], 0)

        #line_y is for displaying the line
        line_y = y
        for i in range(len(outlaws)):
            aoe_hit = aoe_line.collidepoint(outlaws[i])
            if aoe_hit == 1:
                pending_removal_outlaws.append((outlaws[i][0]-outlaw_speed, outlaws[i][1]))
        for i in range(len(speedy)):
            aoe_hit = aoe_line.collidepoint(speedy[i])
            if aoe_hit == 1:
                pending_removal_speedy.append((speedy[i][0]-speedy_speed, speedy[i][1]))
        for i in range(len(brutes)):
            aoe_hit = aoe_line.collidepoint(brutes[i])
            if aoe_hit == 1:
                pending_removal_brutes.append((brutes[i][0]-brute_speed, brutes[i][1]))
        for i in range(len(shifters)):
            aoe_hit = aoe_line.collidepoint(shifters[i])
            if aoe_hit == 1:
                pending_removal_shifters.append((shifters[i][0]-shifter_speed, shifters[i][1]))
        for i in range(len(chiefs)):
            aoe_hit = aoe_line.collidepoint(chiefs[i])
            if aoe_hit == 1:
                pending_removal_chiefs.append((chiefs[i][0]-chief_speed, chiefs[i][1]))

        # Update cooldown
        electro_2_cd = 480

#Time left on the shockwave
shockwave_time = 0
def electro_ult():
    global shockwave_time
    global electro_3_cd
    if electro_3_cd == 0:
        shockwave_time = 360
        # Update cooldown
        electro_3_cd = 1800



# ---------------------------

#Display entry screen with the left HUD and faction select
def entry_screen():
    #Health
    global faction
    global total_health
    global current_health
    #faction being viewed - 0 means none
    view = 0

    play = True
    while play and faction == 0:
        global current_faction_colour
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    play = False
                elif faction == 0 and view != 0 and event.key == K_BACKSPACE:
                    view = 0
            elif event.type == QUIT:
                play = False
            elif event.type == MOUSEBUTTONDOWN:
                if faction == 0:
                    #If a faction has not been selected yet (i.e. On Faction Selection Screen)
                    select_1_hit = select_button_1.collidepoint(event.pos)
                    select_2_hit = select_button_2.collidepoint(event.pos)
                    select_3_hit = select_button_3.collidepoint(event.pos)
                    select_4_hit = select_button_4.collidepoint(event.pos)
                    view_1_hit = view_button_1.collidepoint(event.pos)
                    view_2_hit = view_button_2.collidepoint(event.pos)
                    view_3_hit = view_button_3.collidepoint(event.pos)
                    view_4_hit = view_button_4.collidepoint(event.pos)
                    if view == 0:
                        if select_1_hit == 1:
                            faction = 1
                            current_faction_colour = (255, 0, 0)
                        elif select_2_hit == 1:
                            faction = 2
                            current_faction_colour = (0, 255, 0)
                        elif select_3_hit == 1:
                            faction = 3
                            current_faction_colour = (0, 0, 255)
                        elif select_4_hit == 1:
                            faction = 4
                            current_faction_colour = (255, 255, 0)
                        elif view_1_hit == 1:
                            view = 1
                        elif view_2_hit == 1:
                            view = 2
                        elif view_3_hit == 1:
                            view = 3
                        elif view_4_hit == 1:
                            view = 4
                    else:
                        back_button_hit = view_back_button.collidepoint(event.pos)
                        if back_button_hit == 1:
                            view = 0

        # GAME STATE UPDATES
        # All game math and comparisons happen here

        # DRAWING
        screen.fill((175, 175, 175))# always the first drawing command

        # LEFT SCREEN
        left_hud(DEFAULT[0], DEFAULT[1], DEFAULT[2])
        # RIGHT SCREEN
        if faction == 0:
            if view == 0:
                faction_select()
            elif view == 1:
                view_faction1()
                #Back Button
                pygame.draw.rect(screen, (0,0,0), view_back_button, 0)
                back_text = menu_font.render("BACK", True, (175, 0, 175))
                screen.blit(back_text, [310, 653])
            elif view == 2:
                view_faction2()
                #Back Button
                pygame.draw.rect(screen, (0,0,0), view_back_button, 0)
                back_text = menu_font.render("BACK", True, (175, 0, 175))
                screen.blit(back_text, [310, 653])
            elif view == 3:
                view_faction3()
                #Back Button
                pygame.draw.rect(screen, (0,0,0), view_back_button, 0)
                back_text = menu_font.render("BACK", True, (175, 0, 175))
                screen.blit(back_text, [310, 653])
            elif view == 4:
                view_faction4()
                #Back Button
                pygame.draw.rect(screen, (0,0,0), view_back_button, 0)
                back_text = menu_font.render("BACK", True, (175, 0, 175))
                screen.blit(back_text, [310, 653])

        elif faction == 1:
            faction_1_icon(5, 30)
            pygame.draw.rect(screen, (175, 0, 175), [5, 30, 190, 190], 2)
        elif faction == 2:
            faction_2_icon(5, 30)
            pygame.draw.rect(screen, (175, 0, 175), [5, 30, 190, 190], 2)
        elif faction == 3:
            faction_3_icon(5, 30)
            pygame.draw.rect(screen, (175, 0, 175), [5, 30, 190, 190], 2)
        elif faction == 4:
            faction_4_icon(5, 30)
            pygame.draw.rect(screen, (175, 0, 175), [5, 30, 190, 190], 2)

        # Must be the last two lines
        # of the game loop
        pygame.display.flip()
        clock.tick(60)


#Display menu function
def run_menu():
    global running
    global faction
    menu = True
    while menu and faction == 0:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = False
                    running = False
            elif event.type == QUIT:
                menu = False
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                play_hit = play_button.collidepoint(event.pos)
                if play_hit == 1:
                    menu_to_game_transition()
                    entry_screen()


        # GAME STATE UPDATES
        # All game math and comparisons happen here

        # DRAWING
        screen.fill((255, 255, 255))  # always the first drawing command

        #Load wallpaper
        image = pygame.image.load("castle_invasion.jpg")
        screen.blit(image, (0, 0))
        # Title
        title_faction = game_title_font.render("Faction", True, (0, 0, 0))
        title_wars = game_title_font.render("Defence", True, (0, 0, 0))
        screen.blit(title_faction, [335, 5])
        screen.blit(title_wars, [320, 90])

        # BUTTON
        #Play button
        pygame.draw.ellipse(screen, (0, 0, 0), play_button, 0)
        play_text = menu_font.render("PLAY", True, (255, 255, 0))
        screen.blit(play_text, [460, 735])

        # Must be the last two lines
        # of the game loop
        pygame.display.flip()
        clock.tick(60)

#Used to do the below transition
transition_time = 60
y_pos = 90
def menu_to_game_transition():
    global transition_time
    global y_pos
    y_pos = 90
    transition_time = 60
    while transition_time > 0:
        # #Load wallpaper
        image = pygame.image.load("castle_invasion.jpg")
        screen.blit(image, (0, 0))
        # Title
        title_faction = game_title_font.render("Faction", True, (0, 0, 0))
        title_wars = game_title_font.render("Defence", True, (0, 0, 0))
        screen.blit(title_faction, [335, 5])
        screen.blit(title_wars, [320, y_pos*1.1])
        y_pos *= 1.1
        #Update transition_time
        transition_time-=1
        pygame.display.flip()
        clock.tick(60)

def ending_screen():
    global level
    global current_health

    playing = True
    won = False
    y_position = 1
    while playing:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False
            elif event.type == QUIT:
                playing = False
        #Test if user won
        if level >= 11:
            won = True

        #DRAW
        screen.fill((255,255,255))
        # Different ending screens depending on how the game concludes

        if won:
            #Victory wallpaper
            image = pygame.image.load("victory_wallpaper.jpg")
            screen.blit(image, (0, 0))
            #Victory text
            end_text = game_title_font.render("Victory!", True, (0, 70, 0))
            #Bits - Rain/Hail
            for i in range(85):
                rand_x = random.randint(0, 1000)
                rand_y = random.randint(0, 800)
                pygame.draw.circle(screen, (255, 255, 255), [rand_x, rand_y], 1)
        else:
            #Defeat wallpaper
            image = pygame.image.load("defeat_wallpaper.jpg")
            screen.blit(image, (0, 0))
            #Defeat text
            end_text = game_title_font.render("Defeat...", True, (170, 0, 0))
            #Bits - Moths concentrated on lamp
            for i in range(85):
                rand_x = random.randint(250, 400)
                rand_y = random.randint(550, 700)
                pygame.draw.circle(screen, (0, 0, 0), [rand_x, rand_y], 2)
            #Bits - Random moths
            for i in range(170):
                rand_x = random.randint(0, 1000)
                rand_y = random.randint(0, 800)
                pygame.draw.circle(screen, (0, 0, 0), [rand_x, rand_y], 2)
        #Update position
        if y_position <= 800:
            #Display it dropping
            screen.blit(end_text, [320, y_position * 1.1])
            y_position*=1.1
        else:
            #Display at center
            screen.blit(end_text, [320, 340])

        #Display
        pygame.display.flip()
        clock.tick(60)


# ---------------------------
def run_outlaws():
    global outlaw_counter
    global level
    global current_health
    global current_XP
    global required_XP
    global pending_removal_outlaws
    # Add outlaws if outlaw counter is 0
    if outlaw_counter == 0:
        for i in range(level):
            outlaws.append((1000, random.randint(0, 800)))
    # Update current outlaws (Add them for removal if left hud is hit, otherwise move left)
    for i in range(len(outlaws)):
        if outlaws[i][0] <= 200:
            current_health -= 100
            pending_removal_outlaws.append(outlaws[i])
        else:
            outlaws[i] = (outlaws[i][0]-outlaw_speed, outlaws[i][1])
    # Remove everything that needs to be removed from the outlaws
    for i in range(len(pending_removal_outlaws)):
        # Test first (to protect against double clicks)
        if outlaws.__contains__(pending_removal_outlaws[i]):
            outlaws.remove(pending_removal_outlaws[i])
    # Clear the pending
    pending_removal_outlaws.clear()
    # Update the counter
    outlaw_counter = (outlaw_counter + 1) % 120
    # Update Level
    if current_XP >= required_XP:
        level += 1
        current_XP = 0
        required_XP = level * 1000

def run_speedy():
    global speedy_counter
    global level
    global current_health
    global current_XP
    global required_XP
    global pending_removal_speedy
    # Add speedy if speedy counter is 0
    if speedy_counter == 0:
        for i in range(level):
            speedy.append((1000, random.randint(0, 800)))
    # Update current speedy (Add them for removal if left hud is hit, otherwise move left)
    for i in range(len(speedy)):
        if speedy[i][0] <= 200:
            current_health -= 500
            #Remove by value and not index now
            pending_removal_speedy.append(speedy[i])
        else:
            speedy[i] = (speedy[i][0]-speedy_speed, speedy[i][1])
    # Remove everything that needs to be removed from the speedy
    for i in range(len(pending_removal_speedy)):
        # Test first (to protect against double clicks)
        if speedy.__contains__(pending_removal_speedy[i]):
            speedy.remove(pending_removal_speedy[i])

    # Clear the pending
    pending_removal_speedy.clear()
    # Update the counter
    speedy_counter = (speedy_counter + 1) % 720
    # Update Level
    if current_XP >= required_XP:
        level += 1
        current_XP = 0
        required_XP = level * 1000

def run_brutes():
    global brute_counter
    global level
    global current_health
    global current_XP
    global required_XP
    global pending_removal_brutes
    # Add brute if brute counter is 0
    if brute_counter == 0:
        for i in range(level):
            brutes.append((1000, random.randint(0, 800)))
    # Update current brutes (Add them for removal if left hud is hit, otherwise move left)
    for i in range(len(brutes)):
        if brutes[i][0] <= 200:
            current_health -= 1000
            pending_removal_brutes.append(brutes[i])
        else:
            brutes[i] = (brutes[i][0]-brute_speed, brutes[i][1])
    # Remove everything that needs to be removed from the outlaws
    for i in range(len(pending_removal_brutes)):
        # Test first (to protect against double clicks)
        if brutes.__contains__(pending_removal_brutes[i]):
            brutes.remove(pending_removal_brutes[i])
    # Clear the pending
    pending_removal_brutes.clear()
    # Update the counter
    brute_counter = (brute_counter + 1) % 480
    # Update Level
    if current_XP >= required_XP:
        level += 1
        current_XP = 0
        required_XP = level * 1000


def run_shifters():
    global shifter_counter
    global level
    global current_health
    global current_XP
    global required_XP
    global pending_removal_shifters
    # Add shifter if shifter counter is 0
    if shifter_counter == 0:
        for i in range(level):
            shifters.append((1000, random.randint(0, 800)))
    # Update current shifters (Add them for removal if left hud is hit, otherwise move left)
    for i in range(len(shifters)):
        if shifters[i][0] <= 200:
            current_health -= 500
            pending_removal_shifters.append(shifters[i])
        else:
            shifters[i] = (shifters[i][0]-shifter_speed, shifters[i][1])
    # Remove everything that needs to be removed from the shifters
    for i in range(len(pending_removal_shifters)):
        #Test first (to protect against double clicks)
        if shifters.__contains__(pending_removal_shifters[i]):
            shifters.remove(pending_removal_shifters[i])
    # Clear the pending
    pending_removal_shifters.clear()
    # Update the counter
    shifter_counter = (shifter_counter + 1) % 600
    # Update Level
    if current_XP >= required_XP:
        level += 1
        current_XP = 0
        required_XP = level * 1000


def run_chiefs():
    global chief_counter
    global level
    global current_health
    global current_XP
    global required_XP
    global pending_removal_chiefs
    # Add chief if chief counter is 0
    if chief_counter == 0:
        for i in range(level):
            chiefs.append((1000, random.randint(0, 750)))
    # Update current chiefs (Add them for removal if left hud is hit, otherwise move left)
    for i in range(len(chiefs)):
        if chiefs[i][0] <= 200:
            current_health -= 2500
            pending_removal_chiefs.append(chiefs[i])
        else:
            chiefs[i] = (chiefs[i][0]-chief_speed, chiefs[i][1])
    # Remove everything that needs to be removed from the chiefs
    for i in range(len(pending_removal_chiefs)):
        #Test first (to protect against double clicks)
        if chiefs.__contains__(pending_removal_chiefs[i]):
            chiefs.remove(pending_removal_chiefs[i])
    # Clear the pending
    pending_removal_chiefs.clear()
    # Update the counter
    chief_counter = (chief_counter + 1) % 6000
    # Update Level
    if current_XP >= required_XP:
        level += 1
        current_XP = 0
        required_XP = level * 1000



# ---------------------------
#Shifter rgb
shifter_colour = 0
shifter_direction = 1
#ACTUAL CODE TO RUN GAME
while running and current_health > 0 and level < 11:
    run_menu()
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_1:
                if faction == 1:
                    pyro_1()
                elif faction == 2:
                    naturo_1()
                elif faction == 3:
                    cryo_1()
                else:
                    electro_1(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif event.key == K_2:
                if faction == 1:
                    pyro_2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                elif faction == 2:
                    naturo_2()
                elif faction == 3:
                    cryo_2()
                else:
                    electro_2(pygame.mouse.get_pos()[1])
            elif event.key == K_3:
                if faction == 1:
                    pyro_ult()
                elif faction == 2:
                    naturo_ult()
                elif faction == 3:
                    cryo_ult()
                else:
                    electro_ult()
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            #If the mouse hit ANY target
            hit = False
            #Test if something is hit
            for i in range(len(outlaws)):
                if polymorph_time_counter == 0:
                    if not hit:
                        outlaw_hit = pygame.draw.circle(screen, (0, 0, 0), outlaws[i], 10).collidepoint(event.pos)
                        if outlaw_hit == 1:
                            current_XP+=50
                            pending_removal_outlaws.append((outlaws[i][0]-outlaw_speed, outlaws[i][1]))
                            hit = True
                else:
                    if not hit:
                        outlaw_hit = pygame.draw.circle(screen, (0, 0, 0), outlaws[i], 20).collidepoint(event.pos)
                        if outlaw_hit == 1:
                            current_XP+=50
                            pending_removal_outlaws.append((outlaws[i][0]-outlaw_speed, outlaws[i][1]))
                            hit = True
            for i in range(len(speedy)):
                if polymorph_time_counter == 0:
                    if not hit:
                        speedy_hit = pygame.draw.circle(screen, (0, 0, 0), speedy[i], 10).collidepoint(event.pos)
                        if speedy_hit == 1:
                            current_XP+=100
                            pending_removal_speedy.append((speedy[i][0]-speedy_speed, speedy[i][1]))
                            hit = True
                else:
                    if not hit:
                        speedy_hit = pygame.draw.circle(screen, (0, 0, 0), speedy[i], 20).collidepoint(event.pos)
                        if speedy_hit == 1:
                            current_XP += 100
                            pending_removal_speedy.append((speedy[i][0]-speedy_speed, speedy[i][1]))
                            hit = True
            for i in range(len(brutes)):
                if polymorph_time_counter == 0:
                    if not hit:
                        brute_hit = pygame.draw.circle(screen, (0, 0, 0), brutes[i], 25).collidepoint(event.pos)
                        if brute_hit == 1:
                            current_XP+=250
                            pending_removal_brutes.append((brutes[i][0]-brute_speed, brutes[i][1]))
                            hit = True
                else:
                    if not hit:
                        brute_hit = pygame.draw.circle(screen, (0, 0, 0), brutes[i], 50).collidepoint(event.pos)
                        if brute_hit == 1:
                            current_XP += 250
                            pending_removal_brutes.append((brutes[i][0]-brute_speed, brutes[i][1]))
                            hit = True
            for i in range(len(shifters)):
                if polymorph_time_counter == 0:
                    if not hit:
                        shifter_hit = pygame.draw.circle(screen, (0, 0, 0), shifters[i], 15).collidepoint(event.pos)
                        if shifter_hit == 1:
                            current_XP+=100
                            pending_removal_shifters.append((shifters[i][0]-shifter_speed, shifters[i][1]))
                            hit = True
                else:
                    if not hit:
                        shifter_hit = pygame.draw.circle(screen, (0, 0, 0), shifters[i], 30).collidepoint(event.pos)
                        if shifter_hit == 1:
                            current_XP += 100
                            pending_removal_shifters.append((shifters[i][0]-shifter_speed, shifters[i][1]))
                            hit = True
            for i in range(len(chiefs)):
                if polymorph_time_counter == 0:
                    if not hit:
                        chief_hit = pygame.Rect([chiefs[i][0], chiefs[i][1], 50, 50]).collidepoint(event.pos)
                        if chief_hit == 1:
                            current_XP+=500
                            pending_removal_chiefs.append((chiefs[i][0]-chief_speed, chiefs[i][1]))
                            for j in range(level):
                                outlaws.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                                if j%2 == 0:
                                    speedy.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                                if j%4 == 0:
                                    brutes.append(((chiefs[i][0]-chief_speed, random.randint(0,800))))
                                if j%5 == 0:
                                    shifters.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                            hit = True
                else:
                    if not hit:
                        chief_hit = pygame.Rect([chiefs[i][0], chiefs[i][1], 100, 100]).collidepoint(event.pos)
                        if chief_hit == 1:
                            current_XP += 500
                            pending_removal_chiefs.append((chiefs[i][0]-chief_speed, chiefs[i][1]))
                            for j in range(level):
                                outlaws.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                                if j%5 == 0:
                                    speedy.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                                if j%2 == 0:
                                    brutes.append(((chiefs[i][0]-chief_speed, random.randint(0,800))))
                                if j%4 == 0:
                                    shifters.append((chiefs[i][0]-chief_speed, random.randint(0,800)))
                            hit = True
            if hit and faction==1 and healing_attacks!=0:
                if current_health + 100 >= total_health:
                    current_health = total_health
                else:
                    current_health+=100
                #Reduces Coooldowns too
                if pyro_1_cd > 60:
                    pyro_1_cd-=60
                else:
                    pyro_1_cd = 0
                if pyro_2_cd > 60:
                    pyro_2_cd-=60
                else:
                    pyro_2_cd = 0
                if pyro_3_cd > 60:
                    pyro_3_cd-=60
                else:
                    pyro_3_cd = 0
                #Decrease number left
                healing_attacks-=1

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    #SHIFT COLOUR FOR SHIFTERS
    if shifter_colour == 255:
        shifter_direction = -1
        shifter_colour-=1
    elif shifter_colour == 0:
        shifter_direction = 1
        shifter_colour+=1
    else:
        shifter_colour+=shifter_direction

    #Load the enemies
    run_outlaws()
    run_speedy()
    run_brutes()
    run_shifters()
    run_chiefs()

    #Update cds
    if pyro_1_cd > 0:
        pyro_1_cd -= 1
    if pyro_2_cd > 0:
        pyro_2_cd -= 1
    if pyro_3_cd > 0:
        pyro_3_cd -= 1
    if naturo_1_cd > 0:
        naturo_1_cd -= 1
    if naturo_2_cd > 0:
        naturo_2_cd -= 1
    if naturo_3_cd > 0:
        naturo_3_cd -= 1
    if cryo_1_cd > 0:
        cryo_1_cd -= 1
    if cryo_2_cd > 0:
        cryo_2_cd -= 1
    if cryo_3_cd > 0:
        cryo_3_cd -= 1
    if electro_1_cd > 0:
        electro_1_cd -= 1
    if electro_2_cd > 0:
        electro_2_cd -= 1
    if electro_3_cd > 0:
        electro_3_cd -= 1

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command
    # LEFT SCREEN
    if faction!=0:
        left_hud(current_faction_colour[0], current_faction_colour[1], current_faction_colour[2])

    # LEVEL + XP DISPLAY
    level_display()

    # DRAW ENEMIES
    if polymorph_time_counter == 0:
        for i in range(len(outlaws)):
            pygame.draw.circle(screen, (0, 0, 0), outlaws[i], 10)
        for i in range(len(speedy)):
            pygame.draw.circle(screen, (150, 150, 150), speedy[i], 10)
        for i in range(len(brutes)):
            pygame.draw.circle(screen, (150, 0, 0), brutes[i], 25)
        for i in range(len(shifters)):
            pygame.draw.circle(screen, (shifter_colour, shifter_colour, shifter_colour), shifters[i], 15)
        for i in range(len(chiefs)):
            pygame.draw.rect(screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), [chiefs[i][0], chiefs[i][1], 50, 50], 0)
    else:
        for i in range(len(outlaws)):
            pygame.draw.circle(screen, (0, 0, 0), outlaws[i], 20)
        for i in range(len(speedy)):
            pygame.draw.circle(screen, (150, 150, 150), speedy[i], 20)
        for i in range(len(brutes)):
            pygame.draw.circle(screen, (150, 0, 0), brutes[i], 50)
        for i in range(len(shifters)):
            pygame.draw.circle(screen, (shifter_colour, shifter_colour, shifter_colour), shifters[i], 30)
        for i in range(len(chiefs)):
            pygame.draw.rect(screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), [chiefs[i][0], chiefs[i][1], 100, 100], 0)
        polymorph_time_counter-=1

    #Draw circle for Pyro's ability 2
    if circle_time > 0:
        pygame.draw.circle(screen, (12*circle_time, 6*circle_time, 0), [circle_x, circle_y], 100)
        circle_time-=1

    #Apply healing for Cryo's ability 1
    if cryo_time > 0:
        if current_health!=total_health:
            current_health+=2
        cryo_time-=1

    #Apply slow for Cryo's ability 2
    if slow_time > 0:
        outlaw_speed = 0.25
        speedy_speed = 1.25
        brute_speed = 0.125
        shifter_speed = 0.25
        chief_speed = 0.125
        slow_time-=1
    else:
        outlaw_speed = 1
        speedy_speed = 5
        brute_speed = 0.5
        shifter_speed = 1
        chief_speed = 0.5

    #Apply freeze for Cryo's untimate
    if freeze_time > 0:
        outlaw_speed = 0
        speedy_speed = 0
        brute_speed = 0
        shifter_speed = 0
        chief_speed = 0
        freeze_time-=1

        outlaw_counter-=1
        speedy_counter-=1
        brute_counter-=1
        shifter_counter-=1
        chief_counter-=1



    #Draw Line for Electro's ability 2
    if line_time > 0:
        pygame.draw.rect(screen, (255, 255, 0), [200, line_y-8, 800, 16], 0)
        line_time-=1

    #Apply shockwave purge for Electro's Ultimate
    if shockwave_time > 0:
        aoe_circle = pygame.draw.circle(screen, (255, 255, 0), [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]], 100)
        for i in range(len(outlaws)):
            aoe_hit = aoe_circle.collidepoint(outlaws[i])
            if aoe_hit == 1:
                pending_removal_outlaws.append((outlaws[i][0]-outlaw_speed, outlaws[i][1]))
        for i in range(len(speedy)):
            aoe_hit = aoe_circle.collidepoint(speedy[i])
            if aoe_hit == 1:
                pending_removal_speedy.append((speedy[i][0]-speedy_speed, speedy[i][1]))
        for i in range(len(brutes)):
            aoe_hit = aoe_circle.collidepoint(brutes[i])
            if aoe_hit == 1:
                pending_removal_brutes.append((brutes[i][0]-brute_speed, brutes[i][1]))
        for i in range(len(shifters)):
            aoe_hit = aoe_circle.collidepoint(shifters[i])
            if aoe_hit == 1:
                pending_removal_shifters.append((shifters[i][0]-shifter_speed, shifters[i][1]))
        for i in range(len(chiefs)):
            aoe_hit = aoe_circle.collidepoint(chiefs[i])
            if aoe_hit == 1:
                pending_removal_chiefs.append((chiefs[i][0]-chief_speed, chiefs[i][1]))
        shockwave_time-=1

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)

#Display screen end
ending_screen()
pygame.quit()
