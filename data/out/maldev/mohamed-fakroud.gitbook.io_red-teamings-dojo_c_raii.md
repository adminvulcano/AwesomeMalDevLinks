# https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii

![Page cover](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/~gitbook/image?url=https%3A%2F%2F615064086-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MXlxki-LGPmhYCBAzg5%252Fuploads%252FtpkaqUXfPOQYxh1O3pnK%252F19jk3p%2520%281%29.jpg%3Falt%3Dmedia%26token%3D2d8fe767-9645-4002-aaef-7a71a3655778&width=1248&dpr=3&quality=100&sign=767310d4&sv=2)

## [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#introduction)    Introduction

While developing offensive security tools (OST) and Windows internals utilities, I quickly learned that resource management can make or break your code. Handle leaks, dangling pointers, and forgotten cleanup calls aren't just bugs, they're security vulnerabilities and operational failures waiting to happen. After debugging one too many tools that crashed due to resource exhaustion or left processes in unstable states, I discovered the elegance and power of **Resource Acquisition Is Initialization (RAII)**.

RAII transformed how I write security tooling. What used to require careful tracking of every `CloseHandle()`, `VirtualFree()`, and cleanup call across multiple error paths became automatic and bulletproof. Whether I'm working with process handles, heap allocations, token impersonation, or critical sections, RAII ensures my resources are properly managed, even when exceptions fly or early returns execute.

This blog post is my attempt to share what I've learned. If you're building Windows security tools, dealing with the Win32 API, or just tired of hunting down resource leaks, I hope this guide helps you as much as RAII has helped me.

**Resource Acquisition Is Initialization (RAII)** is a fundamental C++ programming idiom that ties resource management to object lifetime. The core principle:

- **Acquire resources** in the constructor

- **Release resources** in the destructor

- Resources are automatically managed when objects go out of scope


### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-traditional-dynamic-memory-pattern)    The Traditional Dynamic Memory Pattern

A common programming pattern follows these steps:

1. Allocate memory dynamically

2. Store the memory address in a pointer

3. Use that pointer to work with the memory

4. Deallocate the memory when finished


**The Risk**: If an exception occurs after successful memory allocation but before the `delete` or `delete[]` statement executes, you get a memory leak.

Copy

```
#include <iostream>
#include <stdexcept>

bool someCondition(int scenario)
{
    switch (scenario)
    {
    case 1: return false;
    case 2: return true;
    default: return false;
    }
}

void ProblematicFuntion(int scenario)
{
    int* data = new int(42);

    std::cout << "Value stored: " << *data << '\n';
    std::cout << "Address: " << data << '\n';

    if (someCondition(scenario))
    {
        std::cout << "Exception THROWN!\n";
        throw std::runtime_error("Something went wrong!");
    }

    std::cout << "Function ends normally\n";
    delete data;
}
int main()
{
    try
    {
        ProblematicFuntion(2);
    }
    catch (const std::runtime_error& e)
    {
        std::cout << "Exception caught in main: " << e.what() << '\n';
    }

    return 0;
}
```

**The issue**: If an exception is thrown between `new` and `delete`, the memory is never freed.

**The Solution**: The C++ Core Guidelines recommend managing resources like dynamic memory using **RAII (Resource Acquisition Is Initialization)**.

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-raii-principle)    The RAII Principle

The concept is straightforward: For any resource that must be returned to the system when the program finishes using it, the program should:

- **Use that object as necessary** in your program, then

- **When the function call terminates**, the object goes out of scope

- **The object's destructor automatically releases the resource**


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-three-pillars-of-raii)    The Three Pillars of RAII

Copy

```
class RAIIResource {
public:
    // 1. ACQUIRE in constructor
    RAIIResource() {
        resource = AcquireResource();  // File, memory, handle, lock, etc.
    }

    // 2. RELEASE in destructor
    ~RAIIResource() {
        ReleaseResource(resource);     // Automatic cleanup!
    }

    // 3. PREVENT copying (or implement safely)
    RAIIResource(const RAIIResource&) = delete;
};
```

Copy

```
Resource lifetime is tied to object lifetime:
┌────────────────────────────────────────┐
│ Object Created → Resource Acquired     │
│ Object Destroyed → Resource Released   │
└────────────────────────────────────────┘
```

Most bugs come from this false assumption: "If I have a pointer, I own the memory."

❌ That is not true.

A raw pointer does exactly one thing: It stores an address. That’s it.

- No ownership.

- No lifetime.

- No responsibility.


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-a-raw-pointer-actually-represents)    What a raw pointer actually represents

Copy

```
int* p;
```

This means only: "p can point to an int somewhere."

It does not answer:

- Who allocated it?

- Who deletes it?

- How long it lives?

- Is it valid right now?


A raw pointer is non-owning by default.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#ownership-is-a-contract-not-a-type-unless-you-use-raii)    Ownership is a _contract_, not a type (unless you use RAII)

Ownership means **responsibility**.

If you own a resource, you must:

1. Release it exactly once

2. Release it on **every exit path**

3. Not release it after it’s released

4. Not let someone else release it


Raw pointers **cannot enforce this**.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#concrete-raii-example-custom-smart-pointer)    Concrete RAII Example - Custom Smart Pointer

Copy

```
template<typename T>
class SimpleSmartPtr {
private:
    T* ptr;

public:
    explicit SimpleSmartPtr(T* p = nullptr) : ptr(p) {}

    ~SimpleSmartPtr() {
        delete ptr;
        std::cout << "Memory automatically freed\n";
    }

    SimpleSmartPtr(const SimpleSmartPtr&) = delete;
    SimpleSmartPtr& operator=(const SimpleSmartPtr&) = delete;

    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
};
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#walkthrough-of-the-code-line-by-line)    Walkthrough of the code (line by line)

Copy

```
template<typename T>
class SimpleSmartPtr {
private:
    T* ptr;
```

This is the **raw resource,** RAII does _not_ remove raw resources - it **contains them**.

Copy

```
explicit SimpleSmartPtr(T* p = nullptr) : ptr(p) {}
```

This is the **acquisition** step.

Important observations:

- Ownership is transferred **here**

- After construction, _this object is responsible for deletion_

- Initialization in RAII refers to **object initialization**, not variable assignment


This line is the _moment of responsibility transfer_.

Copy

```
~SimpleSmartPtr() {
    delete ptr;
    std::cout << "Memory automatically freed\n";
}
```

This is the **release** step.

Crucial RAII rule:

> The destructor must _always_ leave the program in a valid state.

That means:

- It must not leak

- It must not throw

- It must tolerate `ptr == nullptr`


Copy

```
SimpleSmartPtr(const SimpleSmartPtr&) = delete;
SimpleSmartPtr& operator=(const SimpleSmartPtr&) = delete;
```

They do **two different but related things**.

1. Deleting the copy constructor:


Copy

```
SimpleSmartPtr(const SimpleSmartPtr&) = delete; //Ownership cannot be duplicated
```

What this _syntactically_ means

- This is the **copy constructor**

- `= delete` tells the compiler: This function is forbidden to exist


If _anyone_ tries to copy your object → **compile-time error**.

Imagine this code **without** deleting the copy constructor:

Copy

```
SimpleSmartPtr<int> a(new int(42));
SimpleSmartPtr<int> b = a;   // copy!
```

**After the copy:**

- `a.ptr` → points to memory

- `b.ptr` → points to **the same memory**


So now you have 2 owners of the same resource

What happens next?

When the scope ends:

1. `b` is destroyed → `delete ptr`

2. `a` is destroyed → `delete ptr` again ❌


That is:

- **Double delete**

- **Undefined behavior**

- **Heap corruption**


1. Deleting copy assignment


Copy

```
SimpleSmartPtr& operator=(const SimpleSmartPtr&) = delete;
```

This blocks a _different_ kind of copy.

Without this, this would compile:

Copy

```
SimpleSmartPtr<int> a(new int(1));
SimpleSmartPtr<int> b(new int(2));

b = a;   // copy assignment
```

What would happen?

Let’s simulate it:

1. `b` already owns memory (`new int(2)`)

2. Assignment overwrites `b.ptr` with `a.ptr`

3. Original memory owned by `b` is **leaked**

4. Now both `a` and `b` point to same memory

5. Double delete later 💥


So copy assignment causes:

- Memory leak

- Double delete

- Ownership confusion


This is **ownership enforcement**.

Why this matters:

- Two objects owning the same pointer = double delete

- RAII _requires_ clear ownership rules


By deleting copy:

- Ownership is exclusive

- Cleanup happens exactly once


This is **fundamental RAII design**, not optional.

Copy

```
T& operator*() { return *ptr; }
T* operator->() { return ptr; }
```

These give the illusion: "This behaves like a pointer”

But importantly:

- The pointer is **guarded**

- You cannot forget to delete it


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#code-using-our-smart-pointer)    Code using our smart pointer

Copy

```
#include <iostream>
#include <stdexcept>

bool someCondition(int scenario)
{
    switch (scenario)
    {
    case 1: return false;
    case 2: return true;
    default: return false;
    }
}

void ProblematicFuntion(int scenario)
{
    // RAII: ownership starts here
    SimpleSmartPtr<int> data(new int(42));

    std::cout << "Value stored: " << *data << '\n';
    std::cout << "Address: " << data.operator->() << '\n';

    if (someCondition(scenario))
    {
        std::cout << "Exception THROWN!\n";
        throw std::runtime_error("Something went wrong!");
    }

    std::cout << "Function ends normally\n";
}
int main()
{
    try
    {
        ProblematicFuntion(2);
    }
    catch (const std::runtime_error& e)
    {
        std::cout << "Exception caught in main: " << e.what() << '\n';
    }

    return 0;
}
```

Copy

```
SimpleSmartPtr<int> data(new int(42));
```

That single line does **three things**:

1. Allocates memory (`new int(42)`)

2. Transfers ownership to `SimpleSmartPtr`

3. Guarantees cleanup via destructor


There is **no**`delete` **anywhere** in the function ProblematicFuntion().

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-happens-when-the-exception-is-thrown-step-by-step)    What happens when the exception is thrown (step-by-step)

Let’s simulate `scenario == 2`.

1. `data` is constructed on the stack
→ owns the heap memory

2. `throw std::runtime_error(...)` executes

3. Stack unwinding begins
→ `ProblematicFuntion` is exited

4. Local objects are destroyed
→ `~SimpleSmartPtr()` is called

5. Destructor executes:







Copy

```
delete ptr;
```

6. Memory is freed **before** control reaches `main`


This happens **even though you never wrote cleanup code in the function**.

That’s RAII.

circle-info

`SimpleSmartPtr` is:

- **Single-owner**

- **Non-copyable**

- **Exception-safe**


But it is **not**:

- Array-safe (`delete[]`)

- Move-enabled

- Thread-safe


### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#lvalue-vs-rvalue)    lvalue vs rvalue

- **lvalue** → has an **identity** (you can point to it, it lives somewhere)

- **rvalue** → is a **temporary value** (no stable identity)


The names come from _left-hand side_ and _right-hand side_ of assignments, but modern C++ meaning is a bit deeper.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#lvalue)    lvalue

An **lvalue**:

- Has a **memory address**

- Can usually appear on the **left side of**`=`

- Represents an object that persists beyond a single expression


Copy

```
int x = 10;
```

- `x` → **lvalue**

- `10` → **rvalue**


You can take the address of an lvalue:

Copy

```
int* p = &x;   // OK
```

More lvalue examples:

Copy

```
int a = 5;
a = 6;                 // OK
std::string s = "hi";
s[0] = 'H';            // OK
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#rvalue)    rvalue

An **rvalue**:

- Is a **temporary**

- Usually **cannot** be assigned to

- Often destroyed at the end of the expression


Copy

```
int y = x + 3;
```

- `x + 3` → **rvalue**


You cannot take its address:

Copy

```
int* p = &(x + 3);  // ❌ error
```

More rvalue examples:

Copy

```
5
x + 1
std::string("hello")
```

This fails:

Copy

```
x + 1 = 7; // ❌ not allowed
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#lvalue-reference-t-and)    lvalue reference (`T&`)

A **reference that can bind only to lvalues**:

Copy

```
int x = 10;
int& ref = x;     // OK

int& ref2 = 10;   // ❌ error
```

Use this when:

- You want to **modify an existing object**

- You want to avoid copying


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#rvalue-reference)    rvalue reference

Introduced in **C++11**.

An **rvalue reference**:

- Binds to **temporaries**

- Enables **move semantics**


Copy

```
int&& r = 10;     // OK
```

But this is tricky:

Copy

```
int&& r = x;      // ❌ error (x is an lvalue)
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#why-this-exists)    Why this exists

To _steal resources_ from temporaries instead of copying:

Copy

```
std::string makeStr();

std::string s = makeStr();  // move instead of copy
```

circle-info

**A named rvalue reference is an lvalue**

Copy

```
int&& r = 10;

r = 20;       // OK
```

Because `r` has a name → it has identity → **lvalue**

**Functions that return by reference return an lvalue, and functions that return by value return an rvalue.**

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#key-idea-one-line)    Key idea (one line)

👉 **The return** _**type**_ **decides the value category of the function call expression.**

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#case-1-return-by-value-rvalue-prvalue)    Case 1: Return **by value** → rvalue (prvalue)

Copy

```
int f() {
    return 10;
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-is-f)    What is `f()`?

- `f()` produces a **temporary value**

- No stable identity

- You cannot assign to it


Copy

```
int x = f();   // OK
f() = 5;       // ❌ illegal
```

So:

> `f()` is an **rvalue**

Why?
Because returning by value means **“give me a copy / temporary”**, not a specific object.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#case-2-return-by-lvalue-reference-lvalue)    Case 2: Return **by lvalue reference** → lvalue

Copy

```
int global = 42;

int& g() {
    return global;
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-is-g)    What is `g()`?

- `g()` refers to a **real, named object**

- Has identity

- Can be assigned to


Copy

```
g() = 100;     // ✅ OK
int* p = &g(); // ✅ OK
```

So:g() is an lvalue

Why?
Because returning `T&` means **“this function call** _**is**_ **an object”**, not a temporary.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#case-3-return-by-rvalue-reference-xvalue)    Case 3: Return **by rvalue reference** → xvalue

Copy

```
int&& h() {
    static int x = 5;
    return std::move(x);
}
```

Now:

Copy

```
h() = 20;          // OK
int&& r = h();     // OK
```

- Has identity

- Marked as _expiring_

- Move allowed


So: h() is an xvalue (a kind of rvalue)

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-rule)    The rule

Function return type

`f()` is

`T`

rvalue

`T&`

lvalue

`T&&`

xvalue

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#why-the-language-does-this)    Why the language does this

Because the compiler must answer questions like:

- Can I assign to `f()`?

- Can I take `&f()`?

- Should I call copy or move?

- Which overload should I pick?


And the **return type answers all of those**.

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#concrete-mental-model)    Concrete mental model

Returning by value

- Here’s a **value**, do whatever you want with it.


Returning by reference

- Here’s **the actual object**, go talk to it.


Returning by rvalue reference

- Here’s the object, but **it’s about to be looted**.


## [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#raii-wrapper-for-virtualalloc-virtualfree)    RAII wrapper for VirtualAlloc/VirtualFree

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-problem-does-this-solve)    What Problem Does This Solve?

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-old-c-style-way)    The Old C-Style Way

Copy

```
void DoSomething() {
    // Allocate memory manually
    void* memory = VirtualAlloc(nullptr, 1024,
                                MEM_RESERVE | MEM_COMMIT,
                                PAGE_EXECUTE_READWRITE);

    if (!memory) {
        printf("Allocation failed!\n");
        return;  // Early return - OK
    }

    // Use the memory
    if (SomeCondition()) {
        VirtualFree(memory, 0, MEM_RELEASE);  // Must remember to free!
        return;
    }

    if (AnotherCondition()) {
        // OOPS! Forgot to free memory - LEAK!
        return;
    }

    DoWork(memory);

    VirtualFree(memory, 0, MEM_RELEASE);  // Must remember!
}
```

**Problems:**

- ❌ Easy to forget `VirtualFree()`

- ❌ Multiple return paths = multiple places to free

- ❌ If exception thrown, memory leaked

- ❌ No way to transfer ownership safely

- ❌ Boilerplate error checking


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-modern-c-way)    The Modern C++ Way

Copy

```
void DoSomething() {
    // Allocation + error checking in one line!
    VirtualMemory memory(1024, PAGE_EXECUTE_READWRITE);

    // Automatic cleanup no matter how we exit!
    if (SomeCondition()) {
        return;  // memory freed automatically
    }

    if (AnotherCondition()) {
        return;  // memory freed automatically
    }

    DoWork(memory.get());

    // memory freed automatically at end of scope
}
```

**Benefits:**

- ✅ Impossible to forget cleanup

- ✅ Exception-safe automatically

- ✅ Ownership is clear

- ✅ Transfer ownership with move semantics

- ✅ Zero runtime overhead


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#why-raii-is-powerful)    Why RAII Is Powerful

Copy

```
cpp{
    VirtualMemory mem(1024, PAGE_READWRITE);  // ← Constructor runs

    // Use mem...

    if (error) {
        throw std::runtime_error("Error!");   // Exception thrown!
        // Stack unwinding happens...
        // ~VirtualMemory() called automatically!
        // Memory freed even though exception thrown!
    }

}  // ← Destructor runs here (normal exit)
```

circle-info

**Key insight:** C++ guarantees destructors are called during stack unwinding!

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#constructor-deep-dive)    Constructor Deep Dive

Copy

```
VirtualMemory(SIZE_T size, DWORD protect)     // 1. Parameters
    : m_size(size)                             // 2. Member initializer list
{
    m_ptr = ::VirtualAlloc(nullptr, size,      // 3. Constructor body
                          MEM_RESERVE | MEM_COMMIT,
                          protect);
    if (!m_ptr) {                              // 4. Error checking
        throw std::runtime_error(              // 5. Exception on failure
            std::format("VirtualAlloc failed: 0x{:08X}",
                       ::GetLastError())
        );
    }
}
```

**Why use initializer list instead of assignment?**

Copy

```
// ❌ Less efficient - default construct then assign
VirtualMemory(SIZE_T size) {
    m_size = size;  // Default construct m_size (=0), then assign
}

// ✅ More efficient - direct initialization
VirtualMemory(SIZE_T size)
    : m_size(size)  // Directly initialize m_size with value
{
}
```

For primitives like `SIZE_T`, same performance. But for objects:

Copy

```
class MyClass {
    std::string m_name;

public:
    // ❌ Inefficient
    MyClass(const std::string& name) {
        m_name = name;  // 1. Default construct empty string
                        // 2. Copy assign name into it
                        // = 2 operations!
    }

    // ✅ Efficient
    MyClass(const std::string& name)
        : m_name(name)  // Direct copy construction
                        // = 1 operation!
    {
    }
};
```

circle-info

**Always initialize in declaration order!**

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#destructor-deep-dive)    Destructor Deep Dive

Copy

```
~VirtualMemory() {
    if (m_ptr) {                              // 1. Check if resource owned
        ::VirtualFree(m_ptr, 0, MEM_RELEASE); // 2. Release it
    }
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#why-check-if-m_ptr)    Why Check `if (m_ptr)`?

**Scenario: Moved-from object**

Copy

```
VirtualMemory mem1(1024, PAGE_READWRITE);  // mem1.m_ptr = valid address

VirtualMemory mem2 = std::move(mem1);      // mem1.m_ptr = nullptr (moved!)
                                           // mem2.m_ptr = valid address

// Both destructors will be called:
// 1. ~mem1() called - m_ptr is nullptr, skips VirtualFree ✓
// 2. ~mem2() called - m_ptr is valid, frees memory ✓
```

Without the check:

Copy

```
~VirtualMemory() {
    ::VirtualFree(m_ptr, 0, MEM_RELEASE);  // Undefined behavior if m_ptr == nullptr!
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#destructor-rules)    Destructor Rules

Copy

```
// ✅ DO: Make destructors noexcept (implicitly)
~VirtualMemory() {  // noexcept by default
    if (m_ptr) {
        ::VirtualFree(m_ptr, 0, MEM_RELEASE);
    }
}

// ❌ DON'T: Throw from destructor
~VirtualMemory() {
    if (m_ptr) {
        if (!::VirtualFree(m_ptr, 0, MEM_RELEASE)) {
            throw std::runtime_error("Free failed");  // ❌ NEVER DO THIS!
        }
    }
}
```

**Why?** If an exception is already being handled and destructor throws → `std::terminate()` called!

Copy

```
{
    VirtualMemory mem(1024, PAGE_READWRITE);

    throw std::runtime_error("Error 1");  // Exception in flight

}  // ~VirtualMemory() called during unwinding
   // If it throws "Error 2" → TWO exceptions active!
   // C++ can't handle this → std::terminate() → program dies
```

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#the-rule-of-five)    The Rule of Five

Modern C++ has the **Rule of Five**:

If you define any of these five, you should consider all five:

1. Destructor

2. Copy Constructor

3. Copy Assignment Operator

4. Move Constructor

5. Move Assignment Operator


#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#why-all-five)    Why All Five?

Copy

```
class VirtualMemory {
public:
    // 1. Destructor - We manage a resource
    ~VirtualMemory() {
        if (m_ptr) ::VirtualFree(m_ptr, 0, MEM_RELEASE);
    }

    // If we ONLY define destructor, compiler generates these:
    // 2. Copy Constructor (DANGEROUS!)
    VirtualMemory(const VirtualMemory& other)
        : m_ptr(other.m_ptr),    // ❌ Both objects point to same memory!
          m_size(other.m_size)
    {
    }

    // When objects destroyed:
    // ~VirtualMemory() of copy1 - frees memory
    // ~VirtualMemory() of copy2 - frees SAME memory! DOUBLE FREE! 💥
};
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#solution-delete-copy-implement-move)    Solution: Delete Copy, Implement Move

Copy

```
// 2. Copy Constructor - DELETED
VirtualMemory(const VirtualMemory&) = delete;
// Compiler error if you try to copy

// 3. Copy Assignment - DELETED
VirtualMemory& operator=(const VirtualMemory&) = delete;
// Compiler error if you try to assign

// 4. Move Constructor - IMPLEMENTED
VirtualMemory(VirtualMemory&& other) noexcept
    : m_ptr(other.m_ptr),
      m_size(other.m_size)
{
    other.m_ptr = nullptr;   // Transfer ownership!
    other.m_size = 0;
}

// 5. Move Assignment - IMPLEMENTED
VirtualMemory& operator=(VirtualMemory&& other) noexcept {
    if (this != &other) {
        if (m_ptr) {
            ::VirtualFree(m_ptr, 0, MEM_RELEASE);  // Free old resource
        }
        m_ptr = other.m_ptr;        // Take new resource
        m_size = other.m_size;
        other.m_ptr = nullptr;      // Other no longer owns it
        other.m_size = 0;
    }
    return *this;
}
```

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#move-semantics-explained)    Move Semantics Explained

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#what-is-std-move)    What is std::move?

Copy

```
VirtualMemory mem1(1024, PAGE_READWRITE);
VirtualMemory mem2 = std::move(mem1);  // What does this do?
```

`std::move` **doesn't actually move anything!** It just casts to **rvalue reference**:

Copy

```
template<typename T>
T&& move(T& obj) {
    return static_cast<T&&>(obj);  // Just a cast!
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#move-constructor-breakdown)    Move Constructor Breakdown

Copy

```
VirtualMemory(VirtualMemory&& other) noexcept  // 1. Rvalue reference parameter
    : m_ptr(other.m_ptr),                      // 2. Copy pointer
      m_size(other.m_size)                     // 3. Copy size
{
    other.m_ptr = nullptr;                     // 4. Nullify source!
    other.m_size = 0;
}
```

**Step-by-Step Execution**

Copy

```
void Example() {
    VirtualMemory mem1(1024, PAGE_READWRITE);
    // mem1.m_ptr  = 0x00007FF8A9B0  (allocated memory)
    // mem1.m_size = 1024

    VirtualMemory mem2 = std::move(mem1);
    // Move constructor called:

    // Step 1: Initialize mem2.m_ptr with mem1.m_ptr
    // mem2.m_ptr = 0x00007FF8A9B0  (same pointer)

    // Step 2: Initialize mem2.m_size with mem1.m_size
    // mem2.m_size = 1024

    // Step 3: Nullify mem1.m_ptr
    // mem1.m_ptr = nullptr  (no longer owns memory!)

    // Step 4: Zero mem1.m_size
    // mem1.m_size = 0

    // Result:
    // mem1 is now in "moved-from" state (valid but empty)
    // mem2 owns the memory

}   // Destructors called:
    // ~mem1() - m_ptr is nullptr, does nothing
    // ~mem2() - m_ptr is valid, frees memory
```

**Visual representation:**

Copy

```
Before move:
mem1: [ m_ptr: 0x1000 ] ──→ [ MEMORY BLOCK ]
      [ m_size: 1024  ]

After std::move(mem1):
mem1: [ m_ptr: nullptr ]
      [ m_size: 0      ]

mem2: [ m_ptr: 0x1000 ] ──→ [ MEMORY BLOCK ]
      [ m_size: 1024  ]
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#move-assignment-breakdown)    Move Assignment Breakdown

Copy

```
VirtualMemory& operator=(VirtualMemory&& other) noexcept {
    if (this != &other) {                        // 1. Self-assignment check
        if (m_ptr) {                             // 2. Free existing resource
            ::VirtualFree(m_ptr, 0, MEM_RELEASE);
        }
        m_ptr = other.m_ptr;                     // 3. Take new resource
        m_size = other.m_size;
        other.m_ptr = nullptr;                   // 4. Leave source empty
        other.m_size = 0;
    }
    return *this;                                // 5. Return *this
}
```

**Why Self-Assignment Check?**

Copy

```
if (this != &other) {  // Why this check?
```

**Without it:**

Copy

```
VirtualMemory mem(1024, PAGE_READWRITE);
mem = std::move(mem);  // Self-move!

// Without check:
if (m_ptr) {
    VirtualFree(m_ptr, 0, MEM_RELEASE);  // Free our own memory!
}
m_ptr = mem.m_ptr;  // Copy from ourselves (now nullptr!)
// Memory leaked!
```

**With check:**

Copy

```
if (this != &other) {  // &other points to same object as 'this'
    // Skipped! No-op for self-assignment
}
return *this;  // Object unchanged
```

**Why Return**`*this` **?**

Copy

```
return *this;  // Why?
```

**Enables chaining:**

Copy

```
VirtualMemory mem1(1024, PAGE_READWRITE);
VirtualMemory mem2, mem3;

mem3 = mem2 = std::move(mem1);  // Chaining!
// Expands to:
// mem2.operator=(std::move(mem1))  // Returns mem2
// mem3.operator=(mem2)             // Uses returned mem2
```

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#template-member-functions)    Template Member Functions

Copy

```
template<typename T>
T* as() const noexcept {
    return static_cast<T*>(m_ptr);
}
```

#### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#breaking-down-each-part)    Breaking Down Each Part

**1\. Template Syntax**

Copy

```
template<typename T>  // T is a type parameter
T* as() const noexcept { ... }
```

**How it works:**

Copy

```
VirtualMemory mem(1024, PAGE_READWRITE);

auto* bytes = mem.as<uint8_t>();  // T = uint8_t
// Compiler generates:
// uint8_t* as() const noexcept {
//     return static_cast<uint8_t*>(m_ptr);
// }

auto* ints = mem.as<int>();       // T = int
// Compiler generates:
// int* as() const noexcept {
//     return static_cast<int*>(m_ptr);
// }

struct MyStruct { int x; int y; };
auto* structs = mem.as<MyStruct>();  // T = MyStruct
// Compiler generates:
// MyStruct* as() const noexcept {
//     return static_cast<MyStruct*>(m_ptr);
// }
```

**Each instantiation creates a new function!**

**2\. Return Type**`T*`

Copy

```
template<typename T>
T* as()  // Returns pointer-to-T
```

**Examples:**

Copy

```
mem.as<uint8_t>()   // Returns: uint8_t*
mem.as<int>()       // Returns: int*
mem.as<double>()    // Returns: double*
mem.as<MyStruct>()  // Returns: MyStruct*
```

**3\.**`const` **Member Function**

Copy

```
T* as() const noexcept { ... }
        ^^^^^
```

**What does**`const` **mean here?**

Copy

```
class VirtualMemory {
    void* m_ptr;
    SIZE_T m_size;

public:
    T* as() const {
        // Inside const member function:
        // - 'this' has type: const VirtualMemory*
        // - Can't modify m_ptr or m_size
        // - Can only call other const member functions

        // m_ptr = nullptr;     // ❌ Error! Can't modify
        // m_size = 0;          // ❌ Error! Can't modify

        return static_cast<T*>(m_ptr);  // ✅ OK - not modifying
    }
};

// Usage:
const VirtualMemory mem(1024, PAGE_READWRITE);
auto* ptr = mem.as<int>();  // ✅ OK - as() is const

// Non-const version wouldn't work:
// auto* ptr = mem.get();   // ❌ Error if get() is non-const
```

**Why make it const?**

Copy

```
void ProcessMemory(const VirtualMemory& mem) {
    // mem is const reference
    auto* data = mem.as<uint8_t>();  // ✅ Works because as() is const

    // We can read but not modify the VirtualMemory object
}
```

**4\.**`noexcept` **Specifier**

Copy

```
T* as() const noexcept { ... }
              ^^^^^^^^
```

**Meaning:** This function guarantees it will never throw an exception.

**Benefits:**

Copy

```
// 1. Compiler optimizations
// Compiler knows no exception handling code needed

// 2. STL containers can optimize
std::vector<VirtualMemory> vec;
vec.resize(100);  // Can use noexcept operations for efficiency

// 3. Documentation
// Tells users: "This will never fail"

// 4. static_assert checks
static_assert(noexcept(mem.as<int>()), "Should be noexcept");
```

**Contrast with throwing version:**

Copy

```
// Version that can throw
T* as() const {
    if (!m_ptr) {
        throw std::runtime_error("Invalid pointer");
    }
    return static_cast<T*>(m_ptr);
}
// Compiler generates exception handling code
// STL containers use slower code paths
```

**5\.**`static_cast<T*>`

Copy

```
return static_cast<T*>(m_ptr);
       ^^^^^^^^^^^^^^^^^^^
```

**What is**`static_cast` **?**

C++ has several types of casts:

Copy

```
void* ptr = ...;

// 1. C-style cast (avoid!)
int* p1 = (int*)ptr;  // Unsafe, does anything

// 2. static_cast - compile-time type conversion
int* p2 = static_cast<int*>(ptr);  // ✅ Safe, checked at compile time

// 3. reinterpret_cast - reinterpret bits
int* p3 = reinterpret_cast<int*>(ptr);  // Low-level, dangerous

// 4. dynamic_cast - runtime type checking (polymorphic types)
Derived* p4 = dynamic_cast<Derived*>(base_ptr);  // Runtime check

// 5. const_cast - add/remove const
const int* p5 = ...;
int* p6 = const_cast<int*>(p5);  // Remove const (dangerous!)
```

**Why**`static_cast` **for**`void*` **?**

Copy

```
void* m_ptr;  // void* can point to anything

// static_cast<T*> converts void* to typed pointer
uint8_t* bytes = static_cast<uint8_t*>(m_ptr);  // ✅ Safe
int* ints = static_cast<int*>(m_ptr);           // ✅ Safe

// The cast itself is safe, but using the pointer might not be:
*ints = 42;  // Safe only if m_ptr actually points to int storage!
```

**Why not**`reinterpret_cast` **?**

Copy

```
// static_cast for void* → T* is the standard way
T* p1 = static_cast<T*>(void_ptr);  // ✅ Idiomatic

// reinterpret_cast is for reinterpreting bits (not needed here)
T* p2 = reinterpret_cast<T*>(void_ptr);  // Overkill
```

## [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#full-c-implementation)    Full C++ implementation

Copy

```
class VirtualMemory {
public:
    VirtualMemory(SIZE_T size, DWORD protect)
        : m_size(size)
    {
        m_ptr = ::VirtualAlloc(nullptr, size, MEM_RESERVE | MEM_COMMIT, protect);
        if (!m_ptr) {
            throw std::runtime_error(
                std::format("VirtualAlloc failed: 0x{:08X}", ::GetLastError())
            );
        }
    }

    ~VirtualMemory() {
        if (m_ptr) {
            ::VirtualFree(m_ptr, 0, MEM_RELEASE);
        }
    }

    // Delete copy operations
    VirtualMemory(const VirtualMemory&) = delete;
    VirtualMemory& operator=(const VirtualMemory&) = delete;

    // Allow move operations
    VirtualMemory(VirtualMemory&& other) noexcept
        : m_ptr(other.m_ptr), m_size(other.m_size)
    {
        other.m_ptr = nullptr;
        other.m_size = 0;
    }

    VirtualMemory& operator=(VirtualMemory&& other) noexcept {
        if (this != &other) {
            if (m_ptr) {
                ::VirtualFree(m_ptr, 0, MEM_RELEASE);
            }
            m_ptr = other.m_ptr;
            m_size = other.m_size;
            other.m_ptr = nullptr;
            other.m_size = 0;
        }
        return *this;
    }

    void* get() const noexcept { return m_ptr; }
    SIZE_T size() const noexcept { return m_size; }

    template<typename T>
    T* as() const noexcept { return static_cast<T*>(m_ptr); }

private:
    void* m_ptr{nullptr};
    SIZE_T m_size{0};
};
```

Example 1: Basic Usage

Copy

```
#include "VirtualMemory.h"
#include <cstdint>
#include <exception>
#include <iostream>

int main()
{
	try
	{
		VirtualMemory mem(4096, PAGE_EXECUTE_READWRITE);

		auto* bytes = mem.as<uint8_t>();

		// Write some code (x64 "return 42")
		bytes[0] = 0xB8;  // mov eax, ...
		bytes[1] = 0x2A;  // 42
		bytes[2] = 0x00;
		bytes[3] = 0x00;
		bytes[4] = 0x00;
		bytes[5] = 0xC3;  // ret

		using FuncPtr = int(*)();
		auto func = reinterpret_cast<FuncPtr>(mem.get());
		int res = func();
		std::cout << "Result is: " << res << '\n';
	}
	catch (const std::exception& e)
	{
		std::cerr << "Error: " << e.what();
		return 1;
	}

	return 0;
}
```

Example 2: Move Semantics

Copy

```
#include "VirtualMemory.h"
#include <cstdint>
#include <iostream>
#include <format>

VirtualMemory CreateBuffer(size_t size)
{
	VirtualMemory buffer(size, PAGE_READWRITE);

	auto* bytes = buffer.as<uint8_t>();
	std::memset(bytes, 0xAA, size);
	return buffer;
	// Return value optimization (RVO) or move
}

int main()
{
	VirtualMemory buffer1 = CreateBuffer(1024);

	VirtualMemory buffer2 = std::move(buffer1);
	// buffer1 is now empty (nullptr)
	// buffer2 owns the memory

	// Can safely use buffer2
	auto* data = buffer2.as<uint8_t>();
	std::cout << std::format("First byte: 0x{:02X}", data[0]);  // 0xAA

	return 0;
}
```

### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#modern-c-features-summary)    Modern C++ Features Summary

This class demonstrates:

01. ✅ **RAII** \- Resource management tied to object lifetime

02. ✅ **Move Semantics** \- Efficient transfer of ownership

03. ✅ **Rule of Five** \- Proper special member function handling

04. ✅ **Deleted Functions** \- Prevent unwanted operations

05. ✅ **noexcept** \- Exception guarantees for optimization

06. ✅ **Template Member Functions** \- Generic programming

07. ✅ **const Correctness** \- Immutability guarantees

08. ✅ **In-Class Initializers** \- Default member values

09. ✅ **Uniform Initialization** \- Consistent syntax

10. ✅ **std::format** (C++20) - Type-safe formatting

11. ✅ **Explicit Constructors** \- Prevent implicit conversions

12. ✅ **Scope Resolution** \- Explicit namespace lookup


### [hashtag](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/raii\#conclusion)    Conclusion

This `VirtualMemory` class is a perfect example of modern C++ philosophy:

> **Zero-cost abstractions with maximum safety**

You get:

- ✅ Memory safety (no leaks, no double-free)

- ✅ Exception safety (RAII guarantees cleanup)

- ✅ Move efficiency (no unnecessary copies)

- ✅ Clear ownership semantics

- ✅ **Zero runtime overhead**


All while writing less code and making fewer mistakes than manual C-style management!

[PreviousPolymorphism and Virtual Function Reversal in C++chevron-left](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/c++/polymorphism-and-virtual-function-reversal-in-c++) [NextBridging C++ and x64 Shellcode Development (Windows)chevron-right](https://mohamed-fakroud.gitbook.io/red-teamings-dojo/shellcoding/bridging-c++-and-x64-shellcode-development-windows)

Last updated 21 days ago