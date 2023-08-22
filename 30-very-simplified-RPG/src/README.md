# writeup
The whole idea of this challenge is simple. There is a chest with flag and a boss enemy is guarding it. You have to kill the boss to open the chest. To kill the boss you have to open the chest that is inside the fence.

The challenge could be solved with a little help from this awesome tool https://github.com/Qwokka/Cetus

First you need damage to kill the boss. If you play a bit of the game you will find out the strength is correlated with damage of player. To modify the strength of the player first search for 13 with value type i32 in cetus. Kill 2 skeletons to level up. Search for the new strength value. You will find the address of the strength.

Then you need to get access to the chest in fence. For instance you can achieve this by changing the player's x coordinate. Do notice the hint in console `[B6AWarmHint] Player Rigidbody2D position x:` because it is quite hard to find float. With regards to [unity documentation](https://docs.unity3d.com/ScriptReference/Vector2-x.html), the x coordinate is float. Do note that the float value that cetus found has more decimal places than the value shown in console due to some unknown reason, so it is not possible to search for the exact value of x coordinate. Do use differential search with a bit of creativity to find the correct address.
You should be able to achieve something like this
![image](https://github.com/blackb6a/blackb6a-ctf-2023-challenges/assets/33385719/729af854-c5cc-49e1-a587-a3907679aa7a)

The remaining part is simply move to the location of the boss, kill the boss, open the chest, and get flag. Simple!
