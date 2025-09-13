"""Clean Experiments - A Domain-Driven Design Implementation.

This package implements a clean architecture with domain-driven design principles,
demonstrating best practices for building maintainable, testable, and scalable
Python applications.

Architecture Overview:
    The application follows a modular architecture with clear separation of concerns:

    - **Core Domain**: Foundational domain concepts (Entity, DomainEvent, EventDispatcher)
    - **Account Module**: Complete user management domain with business logic
    - **Clean Architecture Layers**: Proper dependency inversion and separation

Key Components:
    - Domain Entities with rich business logic and event sourcing
    - Value Objects for type safety and validation
    - Repository pattern for data persistence abstraction
    - Use Cases for application logic orchestration
    - Event-driven architecture with domain events
    - Dependency injection container for loose coupling

Module Structure:
    ```
    src/
    ├── container.py          # Dependency injection setup
    ├── root.py              # Application composition root
    └── modules/
        ├── core/            # Core domain infrastructure
        │   └── domain/      # Base entity, events, dispatcher
        └── account/         # User management bounded context
            ├── domain/      # User entity, value objects, events
            ├── repository/  # Data access abstraction
            ├── use_case/    # Application services
            ├── handlers/    # Event handlers
            ├── controllers/ # Web API controllers
            └── config/      # Module configuration
    ```

Design Patterns:
    - **Entity Pattern**: Domain objects with identity and behavior
    - **Value Object Pattern**: Immutable objects representing domain concepts
    - **Repository Pattern**: Data access abstraction
    - **Command-Query Separation**: Separate read and write operations
    - **Domain Events**: Decoupled communication between aggregates
    - **Dependency Injection**: Loose coupling and testability

Examples:
    Creating a user with rich domain validation:
    ```python
    from src.modules.account.domain.user import User, UserProperties

    user = User.create(UserProperties(
        name="John Doe",
        age=25,
        email="john@example.com"
    ))

    # Business logic encapsulated in domain
    is_adult = user.is_adult()  # True
    ```

    Using the dependency container:
    ```python
    from src.container import container
    from src.modules.account.use_case.create_user_use_case import CreateUserUseCase

    create_user = container[CreateUserUseCase]
    user = create_user.execute(UserProperties(...))
    ```

Testing:
    Run the test suite with: `task test`

    The project includes comprehensive tests demonstrating:
    - Domain logic validation
    - Event sourcing behavior
    - Repository patterns
    - Use case orchestration

For more information:
    - See AGENTS.md for development guidelines
    - Check individual module docstrings for detailed API documentation
    - Run `task dev` to start the development server
"""
