


#


```java
// ConsoleRunner.py
| new ConsoleIOHook
| new Engine
| Engine.io_hook = ConsoleIOHook
| Engine.start()

// Engine.start():
| new Thread t /* (target=Engine._main_loop_threaded */
| t.start()

// Engine._main_loop_threaded():
| Engine.io_hook.init()
| Engine.io_hook.start()
| Engine.loadGame()
    | Engine.loader.loadGame()
        | AbstractStatusEffect.loadData()
        | AbstractAmmo.loadData()
        | AbstractArmor.loadData()
        | AbstractTool.loadData()
        | AbstractWeapon.loadData()
        | AbstractItem.loadData()
        | AbstractAttack.loadData()
        | AbstractEnemy.loadData()
        | AbstractCombat.loadData()
        | AbstractInteractable.loadData()
        | AbstractRoom.loadData()
        | AbstractDungeon.loadData()
        | // for each loaded abstract dungeon:
            | dungeon.createInstance()
        | Player.loadData()
| // for each loaded player:
    | Engine.evaluateResult()
        | // moves every player into their saved locations and links input handlers
| // while Engine.running:
    | // run tasks
    | // for each active combat:
        | combat.tick.send()
            | // -> Combat tick
    | // check player inputs
        | // if player id is 0 (engine player)
            | // run input as console command
        | // if player is in combat, forward input to combat's input queue and continue to the next input
        | textPattern.handleInput()
            | // -> textPattern input
        


```




# Combat tick
```java



```




















