## Go commands
`go mod init`: start new module, this will put a "go.mod" file in the current directory

`go get <package>`: install dependency

`go run <module_name>`: Run

`go build <module_name>`: compile executable

## Language basics
### Public and Private members
```go
// business/businessA.go
package business

import "fmt"

type privateBusiness struct{	// private struct only accessible in this package
	name string
}

type PublicBusiness struct {	// public struct exported and accessible from other packages
	name string		// private attribute
	DisplayName string	// public attribute
}

func (pb *PublicBusiness) doSomething(){	// private method
	fmt.Println("doing private business")
}

func (pb *PublicBusiness) DoSomething(){	//pubic method
	fmt.Println("doing public business")
}

func cantTouchThis(){				// private function only accessible in this package
	fmt.Println("This shouldnt be accessible.")
}

func TouchThis(){				// public function exported and accessible from other packages
	fmt.Println("You touched this.")
}

```
Camel case declarations are package private, they cannot be exported and accessed from outside of this package.
Title case declarations are package public, they can be accessed from outside of this package.

### Primitive types
#### String
```go
var str string
str = "hi"

// or 
var str string = "hi"

// or
str: = "Hello"
```

Muilti-line string
```go
str: = `multi-line
string`
```

#### Number
```go
num := 3              // int
num := 3.             // float
num := 3 + 4i         // complex128
num := byte('a')      // byte (alias for uint8)

var u uint = 7        // uint
var p float32 = 22.7  // 32-bit float 
```

Variables declared without an explicit initial value are given their zero value:
- `0` for numeric types
- `false` for the boolean type
- `""` for strings

### Array
Arrays have a fixed size and type:
```go
var numbers [5]int
numbers[0] = 1
numbers[1] = 2
// ...
```
Implicit initialization:
```go
numbers := [...]int{1, 2, 3, 4, 5}
```

### Slice
Slices have a dynamic size.
Create a slice from an array:
```go
arr := [3]int{1, 2, 3}
slice := arr[:]
```
The slice is a "view" pointing at the data in the array. Changing an element in a slice results in the same element change in the array.

Create a slice without an explicit array (Go is going to manage the underlying array automatically):
```go
slice := []int{2, 3, 4}
slice := []byte("hello")
```

Append element to a slice:
```go
slice = append(slice, 4, 42, 27)
```
In this case, Go automatically copy the element from the underlying array and move to a new array, and update the slice to point at the new array.

The length and capacity of a slice s can be obtained using the expressions `len(slice)` and `cap(slice)`, the capacity of a slice is the number of elements in the underlying array.

Create a slice using `make`:
```go
a := make([]int, 5)  // creates a zeroed array with length of 5, returning the slice
b := make([]int, 0, 3) // creates a zeroed array with length/capacity of 5, return the slice with length 0
```

### Map
```go
m := map[string]int{"foo":42}   // initializing a map
m := make(map[string]string)	// initializing using make

fmt.Println(m["foo"])     // accessing a value
m["foo"] = 27             // modifying a value
delete(m, "foo")          // deleting a key
```

### Struct
Defining a struct:
```go
type user struct {
  ID int
  FirstName string
  LastName string
}
```
Initializing a struct:
```go
var u user
u.ID = 1
u.FirstName = "Foo"
fmt.Println(u.ID)
```
Implicit initialization:
```go
u := user {
  ID: 1, 
  FirstName: "Foo",   // note the ending comma is important
}
```

### Pointer
```go
var name *string
fmt.Println(name)   // prints `<nil>`
```

```go
var name *string
name = "me"   // error: cannot assign string to a pointer
*name = "me"  // error: cannot dereference a null pointer that has not been initialized
```

The pointer variable needs to be initialized first:
```go
var name *string = new(string)  // initializes the pointer
*name = "me"                    // works, *name now holds the address of the string
fmt.Println(name)               // prints address
fmt.Println(*fname)             // prints the value: "me"
```
Specify a pointer by preceeding it with `*`, and dereference a pointer also by preceeding it with `*`.

Go provides an addressOf operator `&`:
```go
name := "me"
ptr := &name
fmt.Println(ptr, *ptr)  // prints address and value "me"

name = "you"
fmt.Println(ptr, *ptr)  // prints same address with new value "you"
```

### Const and iota
iota is a incrementing constant within the scope of a `const`:
```go
const (
  first = iota
  second = iota
)
const (
  third = iota
)
func main() {
  fmt.Println(first, second, third)   // prints: 0 1 0
}
```

## Control Flow
### Loop
```go
for n != x {
  // pass
}

for count := 0; count <= 10; count++ {
  fmt.Println(count)
}

entry := []string{"Jack","John","Jones"}
for i, val := range entry {
  fmt.Printf("At position %d, the character %s is present\n", i, val)
}
```

### Conditional
```go
if a > b {
  // pass
} else if a == b {
  // pass
} else {
  // pass
}
```

### Switch
Go switch cases break by default unless marked with `fallthrough` keyword:
```go
switch day {
  case "sunday":
    // pass
    fallthrough // after finishing this case it will also run the next case
   
   case "saturday":
    // pass
    
   default:
    //pass
}
```
`switch` does not have to have a condition, it may be used in place for long if-then-else chains.

### Defer
A defer statement defers the execution of a function until the surrounding function returns.
```go
func main() {
	defer fmt.Println("world")
	fmt.Println("hello")
}
```
Deferred function calls are pushed onto a stack. When a function returns, its deferred calls are executed in last-in-first-out order.

### Function closure
```go
func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			i,
			pos(i),
			neg(-2*i),
		)
	}
}
```
Each `adder()` is bound to its own `sum` variable. [Playground](https://go.dev/tour/moretypes/25).

## Type assertion and checking
Type can be asserted using the `i.(T)` syntax where `i` is an interface and `T` is the type being asserted.
```go
var i interface{} = "hello" // `any` type
s := i.(string)
```
Panic will be triggered if type is incorrect:
```go
var i interface{} = 42
s := i.(string) // panic
```
Type assertion can also return gracefully when type is incorrect:
```go
var i interface{} = 42
s, ok := i.(string) // does not panic, ok is false
```
Composite types can also be checked the same way:
```go
var i interface{} = []string{"a", "b", "c"}

if v, ok := i.([]string); ok {
    fmt.Println("slice of strings:", v)
}
```
Type assertion with switch:
```go
var i interface{} = 42

switch i.(type) {
case int:
    fmt.Println("i is an int")
case int, float64:      // multiple types in one case
    fmt.Println("i is a number")
case string:
    fmt.Println("i is a string")
default:
    fmt.Println("unknown type")
}
```
Using variable in a switch:
```go
var i interface{} = []byte("hello")

switch v := i.(type) {
case []byte:
    fmt.Println(string(v))
case string:
    fmt.Println(v)
}
```

## OOP

```go
type Shape interface {
  Area() float64
  Perimeter() float64
}

type Rectangle struct {
  Length, Width float64
}

func (r *Rectangle) Area() float64 {
  return r.Length * r.Width
}

func (r *Rectangle) Perimeter() float64 {
  return 2 * (r.Length + r.Width)
}

func main() {
  var r Shape = &Rectangle{Length: 3, Width: 4}
  fmt.Printf("Type of r: %T, Area: %v, Perimeter: %v.", r, r.Area(), r.Perimeter())
}
```

### Function vs Method
Functions with a pointer or value argument must take a pointer or value respectively.
On the other hand, methods with pointer or value receivers in both cases can take either a value or a pointer. [Read more](https://go.dev/tour/methods/6)

### Interface Receiver Type
In Go, whether to use a pointer or value receiver depends on the specific use case. Here are some general guidelines:

1. Use a pointer receiver when you need to modify the receiver. In Go, arguments are passed by value. This means that if you use a value receiver, the method will get a copy of the receiver, and any modifications will not affect the original value. If you need to modify the receiver, you should use a pointer receiver.

2. Use a pointer receiver to avoid copying the value on each method call. This can be more efficient if the receiver is a large struct, for example.

3. Use a value receiver if the method does not modify the receiver and the receiver is a small struct or basic type. Value receivers can be simpler to understand because they don't have the potential side effects that come with pointers.

4. If the receiver is a map, func, chan, interface, then use a value receiver, because these types are pointers internally.

5. If your type implements an interface, and you need to use pointer semantics for some methods, then all your methods should have pointer receivers, even if they don’t all need it. This is because interfaces in Go are satisfied with the exact method set.

Read more regarding [which receiver type to use](https://stackoverflow.com/a/27775558/10856743).

## Common Built-in Interfaces
### Stringer
The [`Stringer`](https://pkg.go.dev/fmt#Stringer) interface provides the string description of value from the `fmt` package.
```go
type Stringer interface {
	String() string
}
```
A struct that implements `Stringer` can describe itself as a string:
```go
type Person struct {
	Name string
	Age  int
}

func (p Person) String() string {
	return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
}

func main() {
	a := Person{"Arthur Dent", 42}
	fmt.Println(a)
}
```

### Error
The `error` type is a built-in interface:
```go
type error interface {
    Error() string
}
```
To create a custom error type, we need to define the error type, such as using a struct, and implement the `error` interface:
```go
type ErrNegativeNum struct {
	value float64
}

func (e *ErrNegativeNum) Error() string {
	return fmt.Sprintf("negative number encountered: %v", e.value)
}

func IsPositive(x float64) (bool, error) {

	if x < 0 {
		return false, &ErrNegativeNum{value: x}
	}

	return true, nil
}

func main() {
	_, err := IsPositive(-2)
	fmt.Println(err)
}
```
Note that a call to `fmt.Sprint(e)` inside the `Error` method would have caused an infinite loop. 

Sometimes instead of a struct, the custom error may be extended from a premitive type, such as `float64`. In that case you would want to [cast such an error](https://go.dev/tour/methods/20) back to `float64` first, ie: `fmt.Sprint(float64(v))`.

### Reader
The [`Reader`](https://pkg.go.dev/io#Reader) interface from the `io` package specifies how to read a stream of data:
```go
type Reader interface {
	Read(p []byte) (n int, err error)
}
```
To implement a custom reader, wrap it around an `io.Reader`, and implement the `Reader` interface's `Read` method to modify the stream in some way:
```go
type asteriskReader struct {
	r io.Reader
}

func convertToAsterisk(x byte) byte {
	return '*'
}

func (ar asteriskReader) Read(b []byte) (int, error) {
	n, err := ar.r.Read(b)
	for i := 0; i <= n; i++ {
		b[i] = convertToAsterisk(b[i])
	}
	return n, err
}

func main() {
	s := strings.NewReader("hello!")
	r := asteriskReader{s}
	io.Copy(os.Stdout, &r)
}
```

## Generic
### Generic Function
```go
// Index returns the index of x in s, or -1 if not found.
func Index[T comparable](s []T, x T) int {
	for i, v := range s {
		// v and x are type T, which has the comparable
		// constraint, so we can use == here.
		if v == x {
			return i
		}
	}
	return -1
}

func main() {
	// Index works on a slice of ints
	si := []int{10, 20, 15, -10}
	fmt.Println(Index(si, 15))

	// Index also works on a slice of strings
	ss := []string{"foo", "bar", "baz"}
	fmt.Println(Index(ss, "hello"))
}
```
### Generic Type
```go
// List represents a singly-linked list that holds
// values of any type.
type List[T any] struct {
	next *List[T]
	val  T
}
```

## Concurency

### Goroutine
 Goroutine is an abstraction over OS threads managed by Go. Unlike OS threads that have fixed stack space, Goroutines have dynamic stack size. Prefixing a function call with keyword `go`:
 ```go
 
 // running an anonymous function in a goroutine
 go func() {
  // pass
 }()
 
 func test() {
  // pass
 }
 
 // running the 'test' function in a goroutine
 go test()
 ```

### WaitGroup
A WaitGroup waits for goroutines to finish:
```go
func test(wg *sync.WaitGroup) {
  defer wg.Done()   // performs wg.Done() at end of this function
  // pass
}

funct main() {
  var wg sync.WaitGroup
  wg.Add(1)     // Increment WaitGroup counter by 1
  go test(&wg)
  wg.Wait()     // Wait for goroutines to finish
}
```

### Mutex
Mutex locks memory so they are accessed only by one goroutine at a time:
```go
func test(m *sync.Mutex) {
  m.Lock()
  // pass
  m.Unlock()
}

funct main() {
  var m sync.Mutex
  go test(&m)
}
```
See Tour of Go Web Crawler [example](https://goplay.tools/snippet/d0ppHE3ZtIA).

RWMutex is less efficient than regular Mutex, but useful for providing asymmetrical read/write access locking:
```go
func testRead(m *sync.RWMutex) {
  m.RLock()
  // pass
  m.RUnlock()
}

func testWrite(m *sync.RWMutex) {
  m.Lock()
  // pass
  m.Unlock()
}

func main() {
  var m sync.RWMutex
  go testRead(&m)
  go testWrite(&m)
}
```

### Channel
Channels are concurrency-safe communication objects, used in goroutines.
```go
func main() {
  wg := &sync.WaitGroup{}
  ch := make(chan int)
  
  wg.Add(2)
  
  go func(ch chan int, wg *syncWaitGroup){
    fmt.Println(<-ch)
    wg.Done()
  }(ch, wg)
  
  go func(ch chan int, wg *sync.WaitGroup){
    ch <- 42
    wg.Done()
  }(ch, wg)
  
  wg.Wait()
}
```
Sending to and receiving from unbuffered channels are blocking actions. In the above example, `ch <- 42` would be a blocking action if nothing is reading from this channel (ie `fmt.Println(<-ch)`).

Sometimes we need to iterate through a channel that is used by other go routines. The channel needs to be closed after the other go routines have finished running. We can facilitate this by using `WaitGroup`:
```go
func main() {
	ch := make(chan string)
	var wg sync.WaitGroup

	wg.Add(2)
	go func() {
		defer wg.Done()
		ch <- "hello"
	}()
	go func() {
		defer wg.Done()
		ch <- "world"
	}()

	go func() {
		wg.Wait()
		close(ch)
	}()

	for msg := range ch {
		fmt.Println(msg)
	}
}
```
Note that the `wg.Wait()` and closing of the channel happens in yet another go routine instead of the main thread, this is necessary because the `wg.Wait()` is blocked by `wg.Done()` from other go routines, which are also blocked by the main thread waiting to receive from the channel, causing the deadlock. By putting `wg.Wait()` in a separate routine from what is consuming messages from the channel, we resolved the deadlock. ([Playground](https://goplay.tools/snippet/PCZdxV7oF8O))

A few things to keep in mind when working with Channel [Read more](https://dave.cheney.net/2014/03/19/channel-axioms):
- A send to a nil channel blocks forever
- A receive from a nil channel blocks forever
- A send to a closed channel panics
- A receive from a closed channel returns the zero value immediately

### Buffered Channel
```go
ch := make(chan int, 2)
```
Sends to a buffered channel block only when the buffer is full. Receives block when the buffer is empty.

### Channel direction
```go
ch := make(chan int)  // created channels are always bidirectional
func myFunc(ch chan int) {...}  // bidirectional channel
func myFunc(ch chan<- int) {...}  //send-only channel
func myFunc(ch <-chan int) {...}  // receive-only channel
```

### Channel close
Only the sender should close a channel, never the receiver. Sending on a closed channel will cause a panic.
```go
close(ch)

fmt.Println(<-ch)   // receiving from a closed channel will return 0

ch <- 42  // sending message to a closed channel will cause panic

msg, ok := <-ch // ok would be false if ch is closed
```

Typical way of checking if a channel is open
```go
if msg, ok := <-ch; ok {
  // pass
}
```

Iteratively read from a channel using `range`:
```go
go func(ch chan<- int, wg *sync.WaitGroup) {
  ch <- 1
  ch <- 2
  ch <- 3
  close(ch)   // this signals for...range ch
  wg.Done()
}

go func(ch <-chan int, wg *sync.WaitGroup) {
  for msg := range ch {
    fmt.Println(msg)
  }
  wg.Done()
}
```
[Playground](https://goplay.tools/snippet/pzLN2UkZCsi).

Channels aren't like files; you don't usually need to close them. Closing is only necessary when the receiver must be told there are no more values coming, such as to terminate a range loop.

### Channel select
The `select` statement lets a goroutine wait on multiple communication operations.
Select cases are ran without gauranteeing order, whichever case with channel available first will be executed. If both are available, one will be executed at random.

Without the `default` case, select cases are blocking. To allow non-blocking behavior for each case, add a default case:
```go
ch1 := make(chan int)
ch2 := make(chan string)

select {
  case i := <-ch1:
    ...
  case ch2 <- "hello":
    ...
  default:
    // use default case for non-blocking select
```

# Common Gotchas
---
## Passing argument by value vs reference
```go
type A struct {
	Value int
}

func main() {
	a := A{Value: 1}
	fmt.Printf("Address of a.Value in main: %p\n", &a.Value)
	fmt.Printf("Main: a.Value = %d\n", a.Value)

	a.Change()
	fmt.Printf("After calling Change(): a.Value = %d\n", a.Value)

	a.Change2()
	fmt.Printf("After Calling Change2(): a.Value = %d\n", a.Value)
}

func (a A) Change() { // by value
	fmt.Printf("Address of a.Value in Change(): %p\n", &a.Value)
	a.Value = 2
}

func (a *A) Change2() { // by ref
	fmt.Printf("Address of a.Value in Change2(): %p\n", &a.Value)
	a.Value = 2
}
```
Output:
```commandline
Address of a.Value in main: 0xc00018a000
Main: a.Value = 1
Address of a.Value in Change(): 0xc00018a008
After calling Change(): a.Value = 1
Address of a.Value in Change2(): 0xc00018a000
After Calling Change2(): a.Value = 2
```
In this example, `Change()` has the argument passed by value while `Change2()` has the argument passed by reference. `Change()` is working with a deep copy of the argument, while `Change2()` is working with the same variable from `main()`.
[Link to Go Playground](https://go.dev/play/p/Uoa8Z9JvM21)

## Implicit initialization
```go
type Params struct {
	a int32
	b int32
}

func work(p Params) {
	fmt.Printf("Working with a=%v, b=%v", p.a, p.b)
}

func main() {
	work(Params{
		a: 47,
	})
}
```
Output:
```commandline
Working with a=47, b=0
```
In this example, struct instance `work` has `b=0` even though we had not specified it during initialization. [Link to Go Playground](https://go.dev/play/p/cn7ncGfPB4b)

Similarly, in the next example:
```go
type Container struct {
	Items map[string]int32
}

func (c *Container) Inspect() {
	fmt.Printf("We have %v items", len(c.Items))
}

func main() {
	var c Container
	c.Inspect()	// works fine with uninitialized Container
}

```
Output:
```commandline
We have 0 items
```
This works fine, because `map[string]int32` is a reference type, and its zero value is `nil`, `len(nil)` just returns zero.
However, if we attempt to insert an item into it:
```go
func (c *Container) Insert(key string, value int32) {
	c.Items[key] = value
}

func main() {
	var c Container
	c.Insert("number", 32)  //build fails
}

```
We would get build failure: `assignment to entry in nil map`. [Link to Go Playground](https://go.dev/play/p/1CA1jfb5gWi)
