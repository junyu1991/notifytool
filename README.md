# notifytool

   基于Linux的inotify机制的服务器异常文件监控工具。主要用于监控web目录下的可疑文件或可以操作，如webshell。还可按照配置文件监控系统软件的使用或指定文件夹及其子目录的变化，如insmod等文件的使用。该工具主要使用Email将可疑的操作以及可疑的文件发送至指定的邮箱，同时会将被监控文件的操作情况写入日志文件中。

## required
>1.Linux Kernel >= 2.6  
>2.pyinotify
