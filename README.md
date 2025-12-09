This is created by Antony Fung, as known as Mathematician in the epic rpg community, to generate info for those who want to estimate how many eternal flames they need.

_.jinwoo._'s Lazy Assistant helper bot's enchanting module uses the code here.

The code uses Markov chain. It will be hard for you to understand the code if you don't know what that is.
There are two functions defined in the code: "info" and "chance".

info has 5 arguments: tier, starting_level, end_flame, step, and plot_it.
It output information like median amount of flames you'll need for tier up, mean, central interval, etc.
tier and starting_level should be pretty self explanatory.
end_flame is how much does the code calculate. Just input a number that represents an amount of flames that should be higher than the amount of flames needed for tier up even for a very unlucky person.
If you're unsure whether the number you input is high enough for an accurate result, look at the plot that the function generates and see whether the right-end tail seem to be touching the ground.
If you input a number that's too high, it may take a long time to run though.
step is how many enchants does it do at once. Type 1 if you are unsure. Type a higher number than 1 to run faster (but less accurate).
plot_it is whether you want to plot the probability density function. By default it will plot it. Input False for plot_it if you don't want that.

chance has 3 arguments: tier, starting_level, flames.
It tells you the probability of ending up in each level after you use up all those flames.
Again, tier and starting_level should be self explanatory.
flames is the number of flames you can use.

Both functions assume that you perform enchantments in an unsealed eternal area, so you'll receive flame refunds.
