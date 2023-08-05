# hookman

> github webhooks manager

you just need run as a command in Linux

## first

    pip install hookman

## second
cd your github project and run 

    hookman --run -d
    
it will run in background

also you can set your `projectdir` like

    hookman --run -d --projectdir /my/github/project




####setting

pidfile=~/hookman.pid
logfile=~/hookman.log

####blog

you can go to our [blog](http://blog.zhanglun.me/2016/08/18/hookman-development-notebook/) to know how to contribute your code.

######Develped by TDD
> you can test it just use `py.test .`
> latest version "0.1.2"

use Apache LICENSE  