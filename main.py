from kesslergame import KesslerGame, Scenario, GamepadController, GraphicsType
from controller_keyboard import KeyboardController


def main():
    scenario = Scenario(
        name="ManetteTest",
        num_asteroids=8,
        map_size=(1000, 800),
        ammo_limit_multiplier=10, # mun limit
        stop_if_no_ammo=True     
    )

    #need controller to playz
    controller = KeyboardController()

    game = KesslerGame(settings={
        "graphics_type": GraphicsType.Tkinter,  # change with pyplot if doesnt work
        "prints_on": True,                      # console info
        "perf_tracker": True                   # perf track
    })

    # Game lauch with 1 controller
    game.run(scenario, [controller])

if __name__ == "__main__":
    main()
