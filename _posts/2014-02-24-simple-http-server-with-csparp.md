---
layout: post
title:  "Simple HTTP Server in C#"
date:   2014-02-24
description: I wrote a simple C# class to serve static files in a given directory. It is easy to use as other known single line HTTP servers for Python, Ruby, Node.js and so on.
tags:
  - web
  - programming
  - C#
---

I was working on a Windows desktop application at work.
This application creates static web sites but I needed a local server to show it to the user before deploying.
Most platforms has one line command to serve given folder, so does Windows.
If you have IIS Express you can run this command to serve the given folder:

```bash
"C:\Program Files (x86)\IIS Express\iisexpress.exe" /path:C:\MyWeb /port:8084
```

However, not all Windows machines have IIS Server enabled by default, I needed another solution for client profiles as well.
Eventually, I wrote a simple C# class called [SimpleHTTPServer](https://gist.github.com/aksakalli/9191056) to serve static files in a given directory.
It is using [System.Net.HttpListener Class](https://msdn.microsoft.com/en-us/library/system.net.httplistener.aspx).

## Creating listener

First, I define a private `HttpListener` member and create a listener for assigned port.


```csharp
private HttpListener _listener;
private int _port;

private void Listen()
{
    _listener = new HttpListener();
    _listener.Prefixes.Add("http://*:" + _port.ToString() + "/");
    _listener.Start();
    while (true)
    {
        try
        {
            HttpListenerContext context = _listener.GetContext();
            Process(context);
        }
        catch (Exception ex)
        {

        }
    }
}
```

This while loop is endless and it process the context in a private method whenever a new context appears.
Since this method is synchronous, your UI would become unresponsive.
That's why we need to run it as a new thread when our `SimpleHTTPServer` is constructed.


```csharp
private Thread _serverThread;


public SimpleHTTPServer(string path, int port)
{
    this.Initialize(path, port);
}

private void Initialize(string path, int port)
{
    this._rootDirectory = path;
    this._port = port;
    _serverThread = new Thread(this.Listen);
    _serverThread.Start();
}
```

It is also important to stop it before exiting the app.
Therefore, another public method is defined to be called before terminating.

```csharp
public void Stop()
{
    _serverThread.Abort();
    _listener.Stop();
}
```

## Processing the request

When a new context appears, `Process` method is called to handle the request.
Like any HTTP server, it should handle path value and also if it is some root path `/` to retrieve the default files.
Thus, a default file lists are defined as constant.

```csharp
private readonly string[] _indexFiles = {
    "index.html",
    "index.htm",
    "default.html",
    "default.htm"
};
```

Besides, for file extensions like `.html`, `.png`, `.js`; a mime type list is needed.

```csharp
private static IDictionary<string, string> _mimeTypeMappings =
  new Dictionary<string, string>(StringComparer.InvariantCultureIgnoreCase) {
        {".asf", "video/x-ms-asf"},
        {".asx", "video/x-ms-asf"},
        {".avi", "video/x-msvideo"},
        {".bin", "application/octet-stream"},
        ...

};        
```

Now we are ready to implement `Process` method.

```csharp
private void Process(HttpListenerContext context)
{
    string filename = context.Request.Url.AbsolutePath;
    Console.WriteLine(filename);
    filename = filename.Substring(1);

    if (string.IsNullOrEmpty(filename))
    {
        foreach (string indexFile in _indexFiles)
        {
            if (File.Exists(Path.Combine(_rootDirectory, indexFile)))
            {
                filename = indexFile;
                break;
            }
        }
    }

    filename = Path.Combine(_rootDirectory, filename);

    if (File.Exists(filename))
    {
        try
        {
            Stream input = new FileStream(filename, FileMode.Open);

            //Adding permanent http response headers
            string mime;
            context.Response.ContentType = _mimeTypeMappings.TryGetValue(Path.GetExtension(filename), out mime) ? mime : "application/octet-stream";
            context.Response.ContentLength64 = input.Length;
            context.Response.AddHeader("Date", DateTime.Now.ToString("r"));
            context.Response.AddHeader("Last-Modified", System.IO.File.GetLastWriteTime(filename).ToString("r"));

            byte[] buffer = new byte[1024 * 16];
            int nbytes;
            while ((nbytes = input.Read(buffer, 0, buffer.Length)) > 0)
                context.Response.OutputStream.Write(buffer, 0, nbytes);
            input.Close();

            context.Response.StatusCode = (int)HttpStatusCode.OK;
            context.Response.OutputStream.Flush();
        }
        catch (Exception ex)
        {
            context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
        }

    }
    else
    {
        context.Response.StatusCode = (int)HttpStatusCode.NotFound;
    }

    context.Response.OutputStream.Close();
}
```



## Putting everything together

Here is the result:

* [Gist for SimpleHTTPServer Class](https://gist.github.com/aksakalli/9191056)

## Usage

It is easy to use as other known single line HTTP servers for Python, Ruby, Node.js and so on. Creating server with auto assigned port:

```csharp
string myFolder = @"C:\folderpath\to\serve";
SimpleHTTPServer myServer;

//create server with auto assigned port
myServer = new SimpleHTTPServer(myFolder);


//Creating server with specified port
myServer = new SimpleHTTPServer(myFolder, 8084);


//Now it is running:
Console.WriteLine("Server is running on this port: " + myServer.Port.ToString());

//Stop method should be called before exit.
myServer.Stop();
```
