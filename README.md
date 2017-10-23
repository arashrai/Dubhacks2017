# Dubhacks2017

## Inspiration

It's 2017, and we are more divided than ever. So many issues have become lines in the sand which divide friends and family, neighbours and co-workers, whole communities torn apart because of some idealogical differences. Worse still, many people do not even want to talk to the "other side," since they assume they are all monsters who you could never hope to hold a conversation with.

That's clearly not true. 
Not everyone who disagrees with you is a monster.

Odds are, they are actually a lot like you. 

And we think that if two people get to know one another prior to finding out where they stand on a hot-button issue, odds are that they could then look past their generalizations, and have a interesting discussion with someone across the aisle.

When we humanize those who we otherwise generalize, we can actually pave a path towards civil discussion, mutual understanding, and most of all, less animosity.

## What it does

AcrossTheAisle matches you with someone who is a lot like you, sharing similar hobbies, interests, and ambitions, but who also disagrees with you on some hot-button issue. But here's the thing: we don't tell you what you disagree on until after you've both had a chance to bond over mutual experiences! That way, when you do find out where you two differ in opinion, maybe a civil, mutually informative discussion of differing opinions can occur :)

## How we built it

The app is run on an AWS EC2 instance and all the data is stored in a MySQL instance running on that EC2 instance. The API for account creation/login is a simple Flask application but the chat utilizes some interesting web sockets technology through Flask-SocketIO in order to smoothen the user chat experience.

The front-end is a light, no-frills React App. Aside from react, the only other package used was socket.io. All the CSS is hand-rolled, and implements a simple version of google's material-ui.

## Challenges we ran into

This was actually our first time using socket.io, so we really didn't understand how it worked. Lots of monkey-patching and hacky-code was used to slap together this project, but in the end, it seems to actually work!

## Accomplishments that we're proud of

We started with a idea, threw together a rough flow outline on a whiteboard, and implemented every single screen we set out to make. We made a fully functioning website in under 24h, and while the code isn't the prettiest, it definitely works :D

## What we learned

sleep deprivation !== good code

3rd party socket.io python libraries === hard

sleeping across 3 office chairs: 3/10

## What's next for AcrossTheAisle

Push it out to the world at large, and see if we can clear out some lines in the sand :)

And on a more technical note:
- Rewrite EVERYTHING
- Get enough data to do some neat correlation analysis
- SECURITY
