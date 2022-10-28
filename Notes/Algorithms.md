# Algorithms

Now that we can represent _inputs_ and _outputs_, we can work on **problem solving**.

What stands between inputs(the problem) and outputs(the solution) are **algorithms**, which basically means _step-by-step instructions for solving our problems_.

---

Let's say we have an old-school phone book which contains names and phone numbers.

- We might open the book and start from the first page, looking for a name one page at a time. This algorithm is correct, since eventually we'll find the name if it's in the book.

- We might flip through the book two pages at a time, but this algorithm would be incorrect since we might skip the page that contains the name.

- Another algorithm would be opening the phone book in the middle, decide wether our name will be in the left half or right half of the book and reduce the size of our problem by half. We can repeat this until we find our name.

We can visualize the efficiency of each algorithms with this chart:

![](https://cs50.harvard.edu/x/2022/notes/0/time_to_solve.png)

- The first algorithm is represented by the red line. The '_time to solve_' increases linearly as the size of the problem increases.

- The second algorithm is represented by the yellow line.

- The third algoritm is represented by the green line. It has a different relationship between the _size of the problem_ and the _time to solve it_.
