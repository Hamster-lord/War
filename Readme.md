![alt text](https://github.com/remance/Masendor/blob/master/pygamelogo.gif?raw=true)

![alt text](https://github.com/remance/Masendor/blob/master/preview.gif?raw=true)

$ Educational and historical wargame simulation made with Pygame. 

There is no main name for the game but rather the name will be based on a major update. 

For video update: https://www.youtube.com/channel/UCgapwWog3mYhkEKIGW8VZtw

If anyone is interested in another similar game like this, there is an interesting game by another developer: https://kaetjaatyy.github.io/devlog/

---------------

$ How to run/compile

If you want to download the release version to test the game, go to release tags (https://github.com/remance/Masendor/releases) and download the zip file. 
To start testing the game run main.py for the source code or main.exe for the release version. 
To compile the source code into exe, I would recommend using main.spec to compile the game. 
The main.spec compile only main.py so you will need to copy gamescript, data, profile folder manually to the distribute folder after.

Check the requirements.txt file for dependency requirements if running with the python source code. 
Also, the game is now optimised based on the pygame 2.0.1 module (much faster than 1.9.6) and python 3.7.9. (may have to use cython later for a huge size battle)

---------------

$ Key features so far

The current state of the game and code performance/readibility: ![alt text](https://github.com/remance/Masendor/blob/master/gamestate.png?raw=true)

Meaning: The revision is looking good. Should be able to continue working on the main update again soon.

$$ History is told by the victor, but sometimes the words of the loser do not fade away

Have you ever find it weird that most historical games follow only a specific version of the story? 
For example, the Normans say they are the underdog in the Battle of Hastings, while the Saxons also say they are the underdog.
Well in this game, all versions of the story are accepted and represented. Every preset historical map will have more than 1 source of information that dictates the army composition, size, even formation and possibly more 

![alt text](https://github.com/remance/Masendor/blob/master/source.gif?raw=true)

$$ Army is led by more than just a king

So many historical wargames have only one leader per army. Not here. Every unit has a leadership structure and every historical battle will have all the named people
that participated in the battle.   

![alt text](https://github.com/remance/Masendor/blob/master/leader.gif?raw=true)

$$ Complex troop statistic system

A lot of simplified soldier statistics yet complexly interchange together that affect combat capability in various ways.

![alt text](https://github.com/remance/Masendor/blob/master/troop.gif?raw=true)

$$ Custom unit creator

Bored of a simple line formation and want to try making weird unit formation? There is a custom unit editor that provides a complete freedom unit design. The custom units can be used in custom battles.

![alt text](https://github.com/remance/Masendor/blob/master/custom.gif?raw=true)

$$ Extremely easy map creation

Most of the strategy map creator requires a degree of learning to use effectively. Well in this game you just need to use paint or any drawing software (gimp, photoshop, etc.) to create a map.
Draw the image with the right colour set and the game will convert them into a playable map. Most other map functions are also very easy to create and modify.

Video demonstration: https://www.youtube.com/watch?v=8Omm-o6Dy60

$$ Encyclopedia and stuff

This game's encyclopedia will have more information than just from the Wikipedia website as long as they can be found that is. 

![alt text](https://github.com/remance/Masendor/blob/master/lore.gif?raw=true)

This function is going to be a headache to write and research. But hopefully, it will provide useful and interesting historical information to players.

---------------

$ Future plan

Ver 0.6 Dream Decision: multiple unit selection/move logic, Battle selection(with different estimation source), preparation and result screen, custom battle, custom unit editor, improve the main menu, Battle of Megiddo, Battle of Mohács

0.6.2 - 0.6.5: custom battle, battle result screen, in-game custom sub-unit editor
 
0.6.6 and 0.6.7: random map generator, start working on Battle of Mohács, Minor battle: 764 Irish abbey war  

0.6.8 and 0.6.9: multiple unit selection/move, also add a border to a selected unit on army selector UI

Ver 0.7 Future Visionary: Fog of War(maybe), queue command, unit form, Dismount/discard, hidden stat, line of sight, battalion information based on hidden vs sight, raise flag/ light torch and recon command, ambush bonus, day-night, Battle of Walaja, Battle of Dorylaeum

Ver 0.8 Authentic Attraction: In-game art, better-looking UI (All hand (and mouse) drawn except for historical image), add intro screen, Battle of Isandlwana, Battle of Hwangsanbeol

Ver 0.9 Gaze of New Life: AI and pathfinding (The most challenging step unless cut corner to the point of braindead AI), final code optimisation before full 1.0

Ver 1 Pax Paradisum: historical battle simulation game, Battle of Waterloo, Battle of Dunsinane, Battle of Yijing, Battle of Jengland

Ver 1 - 1.5: More art, sound effects and in-game music (May need to use royalty-free music since I have no experience in music) + Ingame Encyclopedia at main menu + more historical battles

Ver 1.1: Add dynamic terrain/feature change based on battle effect (damage) and weather, unit mode

Ver 1.2: Siege battle, more complex unit equipment (main hand/off hand, item), Minor battle: Wolf of Paris

Ver 1.3: Deception, False information, scout, espionage warfare, information, Minor battle: Siege of Orleans

Ver 1.6: Commander, strategist and leader duel with dynamic result and event (Move from 0.2.7 as it is not the main priority in the early battle sample yet), transfer leader, Battle of Gaixia

ver 1.7: leader rapport and effect on authority and control mechanic including surrender and betrayal 

Ver 1.8: Deployable Defence (Stakes, Barrier, Camp, Wagon), dynamic squad facing position and maybe "saved" formation that player can rotate in battle, swappable squad position

Ver 1.9: Naval battle

Ver 2.0: Multiplayer battle

Ver 2.1: Begin working on another ruleset setting

Unforeseeable future: forced march (Moved here from 0.2.7 as this feature won't have much used until the game map become much larger than just a single battlefield), Queue command

---------------

For those who have read this far, thank you for your interest in the game. To be honest, every single update begins with how do I even start with this. 
I start developing this game with zero knowledge in video game development let alone how to use pygame. I start learning how to use pygame by tinkering with alien.py in pygame examples folder and keep testing/changing it until it becomes what you can see right now (I keep most video updates on youtube which show the progress of improvement almost from the start). All of the plan I list for the future is the same. I have no idea how to do it, the only thing I have is the picture of what I want to make it look like. Nevertheless, it is fun figuring stuff out and don't let the lack of knowledge stop you from making your own game :P. 
