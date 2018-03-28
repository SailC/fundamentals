# host leader

One of the interviews will be done by a host manager. This person may, or may not, end up being the final hiring manager, but will be able to provide you with information on the different projects, engineering team culture, challenges, etc.


He/she will be asking you about your career history, your job search (why you’re looking, why is LinkedIn interesting, what technologies are you interested in), and an overview of interesting projects you worked on, and your involvement in these projects.

Key points our managers will look into:
* Thinking & problem solving: How do you figure out problems, develop solutions and alternatives, what is your decision making process?  

* Organizational fit: What kind of pace do you work at, what level of sophistication you bring to your current team, are you able to be flexible and learn new things on the fly.

* Motivation:  What is your general work-ethic and self-motivation to apply effort to do the work required?

---

## my goal

I've been working as a software engineer for two years, now I'm very determined to become a `full stack` `web` developer. There are two reasons why I want to do this :

1. `web` means the product I ship will be used by a lot of end users directly. Seeing other people using your product brings a great joy to me.

2. `full stack` means I got the chance to watch the data flowing back-end between the front end and back end and appreciate the beauty of these data intensive application. Backend development helps me understanding how the web services are storing & processing the large amount of data. I also like front end development because it gives me the power of visualizing data and present it to the end users.

So if I can become a good full stack web developer,  I was able to convert my thoughts & ideas to data flows on the backend, and visualize the data flow to the end users.

I think there's never been a better time to learn full stack web development because front end development is becoming more and more like backend development, different technologies are learning & borrowing ideas from each other (node<-> js, react <-> module) and more and more application logic are being shift from backend to frontend, so I think programming both front end & back end is much more fun and exiciting right now.

## career at IBM

So the work I've been doing in IBM in these two years are mostly cloud infrastructure related. Our squad is managing the mesos & marathon cluster to provide a highly available and scalable runtime for the services team to run their containerize apps.

Although the job I'm doing is not web development related, it's more about devops and SRE kind of thing. But I think I learned tons of valuable lessons from managing the mesos & marathon cluster because it shows me the ugly picture of the distributed system. Anything can go wrong at anytime, and I think pager duties calls at midnight is motivating me a lot to understand how the distributed system work and how to make it as fault tolerant as possible.
(replication(5 zones) + partition + monitoring)

Managing mesos & marathon allows me to get a close look at how a distributed resource allocator work . Although I haven't been able to dive deeper enough into the source level of mesos & marathon, I think I had a general idea of how mesos & marathon is achieving the scalability, availability and maintainability.

Doing cluster management also shows me the importance of having automation devops tools to boost the productivity (jenkins, docker container and ansible) and the painful troubleshooting experience during oncall also teaches some good lessons about the importance of logging and metrics.

So the work in Watson platform team is the first time I see the wildness of the distributed computing world and I really appreciate this experience.

## my free time

But I'm more interested in delivering application product than managing the underlying cluster. So I use my free time to teach myself web development.

The first challenge I faced when starting the self-education process is that my web skills are scattered around . On the front end side, I know a bit of html, css, javascript, jQuery as most of the programmers do, and on the back end, I know a bit of python, java and c. Knowing a bit of everything is pretty much the same as knowing nothing.

So the first step I took is to pick a project to work on and changing my technology stack during the process of code refactoring because by applying these technologies to a real project, I can had a true feeling of the pros & cons of a certain technology.

So I started working on the website for my friends kimono store.

I started learning from copying. In the beginning, I simply use bootstrap snippets from everywhere, every time I saw something cool on a bootstrap site, I copy the bootstrap code and try to customize that code to fit into the kimono website. That approach worked, on the surface of the webUI it looks ok, but the code is too ugly. HTML code becomes unmanagable when you copy a bit of everything from others, css rules brought by the bootstrap code is also overwriting the global rules, I have no idea of how to deal with the conflict.

So I decided I've had enough for bootstrap and everything heavy weight, I need a lightweight html & css framework that can help me manaing my code in a cleaner and more elegant way. So I learned a templating system called Jinja in python to organize the htmls and also a lightweight css framework called flexbox to make it easier to arrange the layout of the blocks.  This apporach also worked and the code becomes much cleaner and I finally was able to start writing some css code by my own without copy & pasting the bootstrap code snippets.

The when I started writing JQuery to add some animation and do some client server interaction. But things gets ugly again, so I have html, css, javascript and backend python server and templating system to manage. Each of them share different program style and my mind is doing constant context switch between different programming languages and styles.

One of the worst feeling I had is that the front end programming never gives me the effectiveness and modularity I got from the backend programming language. HTML and css doesn't provide function and module or libraries, everything is in the global namespace and it's really annoying for me to go through the process of learning and tweaking those css rules. But the desire of making my website look nice helped me to continue learning. and luckily I was able to find React.js , a javascript library which makes the front end programming fun again.

With react, I can containerize the html & css code in a react components and compose my UI in a modular fashion. And since js is a programming language, I finally feel like I'm coding again instead of tweak html & css.

With react declarative programming style I was able to manage the UI by simply feeding the data to the state of my UI, and react will render the dom element for me. I don't have to write imperative JQuery to do the explict manipulation of the dom element. This way makes my feeling more like programming in backend because I can focus on manipulating data instead of the dom element.

So by the time I fnished the website, I'm pretty comfortable using react. And then I tried to expand my knowledge about it by appling react native to the mobile app.

In the busgazer app, the statu of the UI is more complex than the website, so I learned redux to manage the state. Redux makes status manage even more convenient by explictly isolate the logic of the data flow from the UI code. With Redux , I was able to build the logical data flow of my front end UI , so I can test the state and actions of my front end data flow even wihout building the actually UI components.

The experience of using react totally changed my feeling about front end programming and now I think both front end and back end development are all about managing the data flows.

## My contribution

I take the lead during upgrading process, without downtime.

## why LinkedIn

-  Some of the most famous open-source technologies such as Kafka, Samza, Rest.li and Voldemort were born in LinkedIn.  Although I haven't got the chance to use it but my limited knowledge about the distributed system seems to tell me that Kafka might be the center of the future application architecture and every data store can flow data to each other via kafa. So linkedin really impressed me by being the pionnior of the distributed data processing

- Linkedin is connecting the world’s professionals to make them more productive and successful, helping people to find their dream jobs, and also enabling them to be great at the jobs they’re already in. Being able to contribute to such a product means a lot to me because it's making this world more productive.

- Linkedin has perhaps the most educated and intelligent end users of all apps. If I can make a feature or product that make these elite users satisfied, it will be a great achievement for me.  
