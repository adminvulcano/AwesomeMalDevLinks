# https://blog.washi.dev/posts/awaitfuscator/

Awaiting the Awaitables - Building the AwaitFuscator

Contents

Here is a scenario you probably have never encountered.
Have you ever decompiled a .NET binary that only consists of a bunch of `await` keywords and nothing else?

Yea me neither. Well… until now I suppose.

The program is fully functional.
It does a bunch of complex things, like asking for input, processing it and producing some output.
Very similar to a normal application:

_The program works fine._

So how is this possible?
How can code consisting of only meaningless-looking `await`s encode the functionality of an entire application?
What would you do to reverse this?

In this post, we will explore the inner workings behind the `async` and `await` keywords, push them to the limits, and write an obfuscator that can turn programs into long chains of `await`s.

[Full Source Code](https://github.com/Washi1337/AwaitFuscator) [Download Crack-Me](https://blog.washi.dev/assets/bin/posts/awaitfuscator/AwaitMe.exe)

## What is Async/Await?

With the release of [version 5.0](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history#c-version-50), C# introduced two new keywords `async` and `await` that completely changed the way we do asynchronous programming.
With these keywords, it is very easy to turn blocking, synchronous operations into non-blocking, asynchronous operations without losing any on readability and maintainability of the code itself.

Consider the following click handler for a download button on a window, that downloads the RSS feed of this blog and displays it:

`public void DownloadButtonOnClick(object? sender, EventArgs e)
{
    var client = new HttpClient();
    string xmlData = client.GetString("https://blog.washi.dev/feed.xml");
    ParseAndDisplayRssFeed(xmlData);
}

`

Ideally, we would like to avoid running this code on the main thread directly, as blocking IO can render our UI unresponsive.
With `async` and `await`, this is very easy to do with very minimal changes to our code:

`public async void DownloadButtonOnClick(object? sender, EventArgs e)
{
    var client = new HttpClient();
    string xmlData = await client.GetStringAsync("https://blog.washi.dev/feed.xml");
    ParseAndDisplayRssFeed(xmlData);
}

`

All we did was mark the method `async`, change the call to `GetStringAsync` and add the `await` keyword in front of it.

It cannot be easier than that!

## What are Awaitable Expressions really?

Only certain types of expressions can be `await`-ed.
The most well-known expressions satisfying this property are expressions of type `Task` or `Task<T>`.
This is because `Task` and `Task<T>` both define a method `GetAwaiter` that returns an instance of the `TaskAwaiter` type, a structure looks a bit like the following:

`public readonly struct TaskAwaiter<TResult> : INotifyCompletion, /* ... */
{
    /* ... */

    public bool IsCompleted { get; }
    public void OnCompleted(Action continuation) { /* ... */ }
    public TResult GetResult() { /* ... */ }

    /* ... */
}

`

Consider again the code that asynchronously downloads the RSS feed:

`string xmlData = await client.GetStringAsync("https://blog.washi.dev/feed.xml");
/* ... remainder of code ... */

`

The `GetStringAsync` method call here returns `Task<string>`.
Behind the scenes, the C# compiler transforms the `await` code into roughly the following:

`TaskAwaiter<string> awaiter = client.GetStringAsync("https://blog.washi.dev/feed.xml").GetAwaiter();
if (!awaiter.IsCompleted)
{
    /* ... code to register a callback that eventually calls OnCompleted... */
    return;
}

string xmlData = awaiter.GetResult();

`

Using the `Task<string>.GetAwaiter` method, it obtains an awaiter that knows whether the asynchronous operation is completed or not, and if not, it registers a callback and exits.
It then follows up with a call to `GetResult` to obtain the resulting `string` value of the operation and continues the execution like normal.

## Creating our own Custom Awaiters

The `Task` type is not special, that is, .NET does not have any special treatment for it.
In fact, `await` is not a runtime feature at all, it is merely syntax sugar for the pattern we just covered.
As long as the type defines a `GetAwaiter` method that returns an object implementing `INotifyCompletion` and exposes the members `IsCompleted`, `AwaitOnCompleted` and `GetResult`, it can be awaited using the `await` keyword.

The interesting thing is that this also works if `GetAwaiter` is an **extension method**, allowing us to [make pretty much every type awaitable](https://devblogs.microsoft.com/pfxteam/await-anything/).
For example, we can define a `GetAwaiter` extension method on `int` that returns a custom awaiter interpreting the integer as the total number of seconds to delay execution:

``// Define an extension method on `int` creating an awaiter.
public static SecondsAwaiter GetAwaiter(this int self) => new(self);

public readonly struct SecondsAwaiter : INotifyCompletion
{
    private readonly TaskAwaiter _awaiter;

    public SecondsAwaiter(int seconds)
    {
        // Interpret the integer as seconds and wait for this amount of time.
        _awaiter = Task.Delay(seconds * 1000).GetAwaiter();
    }

    // Implement the same methods as in TaskAwaiter.
    public bool IsCompleted => _awaiter.IsCompleted;
    public void OnCompleted(Action continuation) => _awaiter.OnCompleted(continuation);
    public void GetResult() => _awaiter.GetResult();
}

``

This renders the following C# completely valid:

`Console.WriteLine("Let's (a)wait a bit before continuing.");

await 3;

Console.WriteLine("This prints after 3 seconds.");

`

And sure enough, the program waits 3 seconds before it prints out the second message:

_Awaiting an integer._

## Abusing Custom Awaiters

There are a lot of cool things we can do with custom awaiters, for good and for bad.

The first thing we are going to explore is the fact that `GetResult` is allowed to have **any return type**.
This allows for some interesting constructions.
Consider the following minimal `int` awaiter that returns the same integer it was provided:

`public static IntAwaiter GetAwaiter(this int self) => new(self);

public readonly struct IntAwaiter(int value) : INotifyCompletion
{
    public bool IsCompleted => true;
    public void OnCompleted(Action continuation) {}
    public int GetResult() => value; // <-- result is the awaited value.
}

`

As expected, the code below now becomes valid C#:

`int x = await 3;
Console.WriteLine(x);

`

However, since the expression `await 3` returns an `int`, and `int` is awaitable by our `IntAwaiter`, we can await it again:

`int x = await await 3;
Console.WriteLine(x);

`

… and again…

`int x = await await await 3;
Console.WriteLine(x);

`

In fact, we can await it as many times as we want, to infinity and beyond:

`int x = await await await await await await await await await await await await await await 3;
Console.WriteLine(x);

`

The program still works fine:

_A chain of integer awaiters._

While this looks pretty funny, in itself it does not really do much.
However, a second interesting property of `GetResult` is that we can also change its implementation to do pretty much anything we want:

`public static IntAwaiter GetAwaiter(this int self) => new(self);

public readonly struct IntAwaiter(int value) : INotifyCompletion
{
    public bool IsCompleted => true;
    public void OnCompleted(Action continuation) {}
    public int GetResult()
    {
        Console.WriteLine("Woa where did I come from?");
        return value;
    }
}

`

Now all of a sudden the following code…

`int x = await 3;
Console.WriteLine(x);

`

… gives us the following output:

_Code hidden behind an `await`._

We can get clever with this.
For example, if we let our `IntAwaiter` return `double`, and also define a `DoubleAwaiter` which in turn returns a `float` that can be awaited by a `FloatAwaiter` and so on…, we can chain awaiters together that each have their own little extra bits of code that they execute in their `GetResult` method:

`public static IntAwaiter GetAwaiter(this int self) => new();
public static DoubleAwaiter GetAwaiter(this double self) => new();
public static FloatAwaiter GetAwaiter(this float self) => new();

public readonly struct IntAwaiter : INotifyCompletion
{
    /* ... */
    public double GetResult() { Console.WriteLine("Who needs actual statements"); return 1337.0; }
}

public readonly struct DoubleAwaiter : INotifyCompletion
{
    /* ... */
    public float GetResult() { Console.WriteLine("when all you need"); return 1337f; }
}

public readonly struct FloatAwaiter : INotifyCompletion
{
    /* ... */
    public void GetResult() => Console.WriteLine("is a little bit of patience!");
}

`

This allows us to write entire programs with nothing but long chains of `await`s:

`await await await 1337;

`

… that produces actual meaningful output:

_Code hidden behind a series of awaits._

## Building the AwaitFuscator

Armed with this knowledge, we now have all the ingredients to build the **AwaitFuscator**: An obfuscator that moves all the code from your methods into awaiters, and produces nothing but long chains of `await` keywords.

_The basic concept of AwaitFuscator._

This is tricky to get right.
We need to exactly replicate the code the C# compiler would generate for `async`/`await`, such that decompilers that pattern match on this also recognize it as something that is awaitable.

### The Async State Machine

Whenever the C# compiler encounters a method marked as `async`, it creates a secondary type implementing a **state machine** that encodes all the wiring logic required to call the right awaiters, and jump to the right code after a successful `await` of an expression.
In particular, this wiring is implemented in a method called `MoveNext` that progresses this state machine.

For example, an awaitfuscated program:

`int x = await 1337;

`

… will be compiled by the C# compiler to a beast of a state machine that looks a bit like this:

``private struct Main_StateMachine : IAsyncStateMachine
{
    public int _state = -1;
    public AsyncTaskMethodBuilder _builder;
    private IntAwaiter _awaiter;
    private int _x;

    /* ... */

    public void MoveNext()
    {
        try
        {
            IntAwaiter awaiter;

            // Check which awaited statement we need to jump back to (if any).
            switch (_state)
            {
                case 0:
                    // Restore awaiter and jump back to where we left off (Block1).
                    awaiter = _awaiter;
                    _awaiter = default(IntAwaiter);
                    state = -1;
                    goto Block1;

                /* ... More awaiters can be handled here ... */

                default:
                    goto Block0;
            }

            Block0:
            // Await the int expression (1337).
            var awaiter = GetAwaiter(1337);
            if (!awaiter.IsCompleted)
            {
                // Instruct the state machine which awaiter is currently active, and exit.
                _state = 0;
                _awaiter = awaiter;
                _builder.AwaitOnCompleted(ref awaiter, ref this);
                return;
            }

            Block1:
            // Get result and assign it to "local" `x`.
            _x = awaiter3.GetResult();
        }
        catch (Exception exception)
        {
            /* ... */
        }
        /* ... */
    }
}

``

It is a lot of code, and initially, it may look weird.
But there is a structure to it.

For every awaited expression, `MoveNext` first checks the awaiter’s `IsCompleted` property.
If `true`, the program just continues as normal.
Otherwise, it stores the awaiter in a field, updates a `state` field indicating which awaiter is currently active and instructs an `AsyncTaskMethodBuilder` to register a callback to the current state machine.
It then exits the `MoveNext` method, achieving the non-blocking behavior.

Once the operation completes asynchronously, the `AsyncTaskMethodBuilder` makes sure the `MoveNext` method is called again.
The `switch` at the beginning of the method then makes sure the right awaiter is selected based on the `state` field and jumps back to where we left off in the code, effectively resuming execution as normal.

Note that local variables are lifted to fields in the state machine, as can be seen with the variable `x`, ensuring that they are also preserved upon exiting and re-entering the `MoveNext` method.

### Maintaining Local Variables across Awaiters

In our current setup, our custom awaiters do not have access to the local variables defined in the original method.
To facilitate this, we move all locals and parameters to an auxiliary `Frame` class that we pass along every awaiter by reference.

For example, consider the following snippet:

`public static void Foo()
{
    string input = Console.ReadLine();
    Console.WriteLine("Hello, " + input);
}

`

We lift the `input` local variable to a field that we put in a class `Frame`:

`class Frame
{
    public string input;
}

`

We can then create an instance of this `Frame` class, and pass it along every time the next awaiter is created.
The awaiters then can operate on this frame object instead, and thus emulate the use of local variables:

`public static Awaiter1 GetAwaiter(this Frame frame) => new(frame);
public static Awaiter2 GetAwaiter(this Awaiter1 awaiter) => new(awaiter.Frame);
/* ... */

public readonly struct Awaiter1(Frame frame) : INotifyCompletion
{
    public Frame Frame = frame;

    public Awaiter1 GetResult()
    {
        Frame.input = Console.ReadLine();
        return this;
    }

    /* ... */
}

public readonly struct Awaiter2(Frame frame) : INotifyCompletion
{
    public Frame Frame = frame;

    public Awaiter2 GetResult()
    {
        Console.WriteLine("Hello, " + Frame.input);
        return this;
    }

    /* ... */
}

`

In the final awaitfuscated method, it then looks like no local variable even exists!

`public static async void Foo()
{
    await await new Frame();
}

`

### Bootstrapping the State Machine

Finally, we need to bootstrap the async state machine.

For methods returning `void`, this is simple.
We just create a new instance of the state machine and start it.
Below is the code that is generated by the C# compiler in such a case:

`public static void Foo()
{
    var stateMachine = default(Foo_StateMachine);
    stateMachine.builder = AsyncVoidMethodBuilder.Create();
    stateMachine.state = -1;
    stateMachine.builder.Start(ref stateMachine);
}

`

Indeed, ILSpy then correctly recognizes it as an async method:

_Decompilation of an `async void` method constructed by AwaitFuscator._

However, C# only allows `async`/`await` to be present in methods returning `void`, `Task` and `ValueTask`, so for anything else, this is a little tricky.
The solution I came up with was to define for every method returning `T` a local function that returns `Task<T>`, and just call its `GetAwaiter` and `GetResult` directly:

`public static int Bar()
{
    return BarAsync().GetAwaiter().GetResult();

    static Task<int> BarAsync()
    {
        var stateMachine = default(Bar_StateMachine);
        stateMachine.builder = AsyncVoidMethodBuilder.Create();
        stateMachine.state = -1;
        stateMachine.builder.Start(ref stateMachine);
        return stateMachine.builder.Task;
    }
}

`

It’s a little less elegant, but it works:

_Decompilation of an `async Task<int>` method constructed by AwaitFuscator._

Unfortunately, dnSpy does not know the concept of local functions yet, but it is good enough for me:

_Decompilation of an `async Task<int>` method constructed by AwaitFuscator._

### Hiding our Awaiters

Even for relatively small methods, we produce a huge amount of awaiters and extension methods.

_AwaitFuscator produces many awaiter structures._

We can get rid of these by marking them with the `[CompilerGenerated]` attribute, and giving them names that resemble anonymous types such as `<>AnonType_1`.
This tricks many decompilers, including ILSpy and dnSpy, into not showing these types and methods at all.

_The use of anonymous types helps hiding our tracks._

Much better!

## The Final End Result

If you did everything right, you end up with applications that function exactly the same as the original, but in a decompiler with standard settings it looks like nothing but a bunch of weird await expressions, making close to zero sense:

_Original versus Awaitfuscated._

And of course, for completion sake, the program works fine as expected:

_An awaitfuscated program, running like normal._

## Limitations

The awaitfuscator, of course, does not come without its obvious limitations:

- **Space Overhead:**
The size of the binary increases a lot after awaitfuscation.
We need to add a lot of awaiter types, a lot of extension methods and huge state machines.

- **Performance Overhead:**
The runtime overhead is actually not bad.
We are not really offloading every expression to another thread, and the state machine and all the awaiters are structures and thus fast/cheap to allocate.
We need a `Frame` object though, and for all non-void methods we need at least one `Task` allocation.

- **Obfuscation Capabilities:**
While the long `await` chains look completely meaningless at first, and every awaitfuscated method will look very similar, we are actually not really hiding or obfuscating code.
A novice reverse engineer would not really know what to do with this immediately, but all code is simply moved to a bunch of awaiters as-is.
While these awaiters are made invisible by default, decompilers like dnSpy and ILSpy have the option to view compiler-generated code as well, making it not a super difficult task (pun intended) to at least infer (parts of) the original code.
Automated deobfuscation may still be a pain to implement though!

- **Exception Handlers:**
While it is possible to also use exception handlers in async contexts, currently Awaitfuscator does not support it, as it significantly complicates the implementation for a quick prototype.
A source-based obfuscator may have helped here, as it would mean I could leverage Roslyn directly, but I felt up for a challenge and wanted to learn how exactly these async machines work.


Despite all of that, this is a fun experiment and can probably be used for some fun CTF challenges or similar.

## Final Words

This was a pretty dumb project :).

Because of its limitations, it probably is not really useful in practice other than for a fun CTF challenge or for educational purposes.
But it does show off the power of the C# compiler when it comes to transforming your code, and confirms once again that the current state-of-the-art .NET decompilers are very pattern-matching based.

I also had a lot of fun creating it!

As always, the full code can be found on GitHub.
Keep in mind it is buggy, likely to crash with inexplicable errors, likely to produce corrupted output files, eat your dog, and do other gruesome things.
But here we are for open science:

[Full Source Code](https://github.com/Washi1337/AwaitFuscator) [Download Crack-Me](https://blog.washi.dev/assets/bin/posts/awaitfuscator/AwaitMe.exe)

Happy hacking and I will `await` your comments in the comment section :^)!

## References

- [https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history#c-version-50](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history#c-version-50)
- [https://dev.to/maxarshinov/a-brief-history-of-asyncawait-264j](https://dev.to/maxarshinov/a-brief-history-of-asyncawait-264j)
- [https://devblogs.microsoft.com/dotnet/how-async-await-really-works/](https://devblogs.microsoft.com/dotnet/how-async-await-really-works/)
- [https://devblogs.microsoft.com/pfxteam/await-anything/](https://devblogs.microsoft.com/pfxteam/await-anything/)

[Anti-Reverse Engineering](https://blog.washi.dev/categories/anti-reverse-engineering/),
[Anti-Decompiler](https://blog.washi.dev/categories/anti-decompiler/)

[anti-reverse-engineering](https://blog.washi.dev/tags/anti-reverse-engineering/) [obfuscation](https://blog.washi.dev/tags/obfuscation/) [dotnet](https://blog.washi.dev/tags/dotnet/) [code-golfing](https://blog.washi.dev/tags/code-golfing/) [decompiler](https://blog.washi.dev/tags/decompiler/)




This post is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
by the author.



Share[Twitter](https://twitter.com/intent/tweet?text=Awaiting%20the%20Awaitables%20-%20Building%20the%20AwaitFuscator%20-%20Washi&url=https%3A%2F%2Fblog.washi.dev%2Fposts%2Fawaitfuscator%2F)[Facebook](https://www.facebook.com/sharer/sharer.php?title=Awaiting%20the%20Awaitables%20-%20Building%20the%20AwaitFuscator%20-%20Washi&u=https%3A%2F%2Fblog.washi.dev%2Fposts%2Fawaitfuscator%2F)[Telegram](https://t.me/share/url?url=https%3A%2F%2Fblog.washi.dev%2Fposts%2Fawaitfuscator%2F&text=Awaiting%20the%20Awaitables%20-%20Building%20the%20AwaitFuscator%20-%20Washi)

## Trending Tags

[reverse-engineering](https://blog.washi.dev/tags/reverse-engineering/) [dotnet](https://blog.washi.dev/tags/dotnet/) [obfuscation](https://blog.washi.dev/tags/obfuscation/) [anti-reverse-engineering](https://blog.washi.dev/tags/anti-reverse-engineering/) [asmresolver](https://blog.washi.dev/tags/asmresolver/) [code-golfing](https://blog.washi.dev/tags/code-golfing/) [decompiler](https://blog.washi.dev/tags/decompiler/) [cil-hacking](https://blog.washi.dev/tags/cil-hacking/) [cil](https://blog.washi.dev/tags/cil/) [native](https://blog.washi.dev/tags/native/)