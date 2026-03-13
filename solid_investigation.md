# SOLID Design Principle Investigation

## Object-Oriented Programming (OOP) Paradigm Characteristics
Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects", which can contain data (attributes) and code (methods). The key characteristics include:
1.  **Encapsulation**: Bundling internal data and methods into a single unit (class) and restricting access to some components.
2.  **Abstraction**: Hiding complex implementation details and showing only the necessary features of an object.
3.  **Inheritance**: Deriving new classes from existing ones, promoting code reuse and hierarchy.
4.  **Polymorphism**: The ability of different classes to respond to the same message/method call in their own way.

## Class Relationships
1.  **Association**: A "uses-a" relationship where objects interact independently (e.g., A teacher and a Student).
2.  **Aggregation**: A "has-a" relationship where the child can exist independently of the parent (e.g., A Library and a Book).
3.  **Composition**: A strong "has-a" relationship where the child cannot exist without the parent (e.g., A House and a Room).
4.  **Inheritance**: An "is-a" relationship (e.g., A Car is a Vehicle).

## Design Patterns
1.  **Strategy Pattern** (Used in this project): Defines a family of algorithms (Analyzers), encapsulates each one, and makes them interchangeable.
2.  **Factory Pattern**: Creates objects without specifying the exact class of object that will be created (e.g., `VisualizerFactory`).
3.  **Dependency Injection**: Passing dependencies (like `IDataLoader`) into a class rather than hard-coding them.

## Clean Coding Techniques
-   **Meaningful Names**: Classes and functions should clearly state what they do (e.g., `PublicationTrendAnalyzer` vs `Analyzer1`).
-   **Single Responsibility**: Functions should do one thing and do it well.
-   **No Magic Numbers**: Use named constants instead of raw numbers.
-   **Error Handling**: Fail gracefully and provide informative error messages.

## SOLID Principles
1.  **Single Responsibility Principle (SRP)**: A class should have one and only one reason to change.
    -   *Application*: `CSVDataLoader` only loads data; `MatplotlibVisualizer` only visualizes.
2.  **Open/Closed Principle (OCP)**: Software entities should be open for extension, but closed for modification.
    -   *Application*: New analyzers can be added by creating a new class implementing `IAnalyzer` without changing the CLI code.
3.  **Liskov Substitution Principle (LSP)**: Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application.
    -   *Application*: Any class implementing `IAnalyzer` works seamlessly with the CLI.
4.  **Interface Segregation Principle (ISP)**: Clients should not be forced to depend upon interfaces that they do not use.
    -   *Application*: We split `IDataLoader`, `IAnalyzer`, and `IVisualizer` so classes only implement what they need.
5.  **Dependency Inversion Principle (DIP)**: Depend upon abstractions, not concretions.
    -   *Application*: The `CLI` class depends on `IDataLoader` (interface), not `CSVDataLoader` (concrete class).
