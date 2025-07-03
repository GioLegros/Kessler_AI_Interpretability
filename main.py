from kesslergame import KesslerGame, Scenario, GamepadController, GraphicsType

def main():
    scenario = Scenario(
        name="ManetteTest",
        num_asteroids=6,         # 
        map_size=(1000, 800),    # 
        ammo_limit_multiplier=1, # mun limit
        stop_if_no_ammo=True     
    )

    #need controller to play
    controller = GamepadController()

    game = KesslerGame(settings={
        "graphics_type": GraphicsType.Tkinter,  # change with pyplot if doesnt work
        "prints_on": True,                      # console info
        "perf_tracker": False                   # perf track
    })

    # Game lauch with 1 controller
    game.run(scenario, [controller])

if __name__ == "__main__":
    main()
