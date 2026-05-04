# Thesis Report

## Price Comparison Tool for E-Commerce Products

---

### Certificate

This is to certify that the project report titled **“Price Comparison Tool for E-Commerce Products”** submitted by **[Your Name]** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Engineering/Technology** is a bonafide record of the project work carried out under my supervision.

---

### Acknowledgements

I express my deep gratitude to my project guide, faculty members, and peers for their support and guidance during the development of this project. Special thanks to the department staff for their technical assistance and encouragement.

---

### Declaration

I hereby declare that this project report is my original work and has not been submitted earlier for the award of any degree, diploma, or certificate.

---

### Abstract

This thesis presents the design, development, and evaluation of a web-based **Price Comparison Tool** that allows users to compare product prices from multiple e-commerce platforms in one place. The system combines a Django REST backend with a React frontend to provide a secure, user-friendly solution for search, wishlist management, and price tracking. The study includes requirements analysis, system design, implementation, testing, and future scope. The application addresses consumer needs for efficient price discovery, improved decision-making, and personalized account management.

---

## Table of Contents

1. Introduction
   1.1 Overview
   1.2 Problem Statement
   1.3 Objectives of the Study
   1.4 Scope of the Project
   1.5 Methodology
   1.6 Tools and Technologies
2. Literature Survey & Review
   2.1 Overview
   2.2 Review of Literature
   2.3 Research Gap
3. Workdone – System Analysis
   3.1 Methodology
   3.2 Identification of Need
   3.3 Preliminary Investigation
   3.4 Feasibility Study
   3.5 Project Planning
   3.6 Software/Hardware Requirement
4. Workdone – System Design
   4.1 Modularization Details
   4.2 Database Design
   4.3 Data Dictionary
   4.4 Data Flow Diagram
   4.5 System Flowchart
   4.6 Program Flowcharts
   4.7 Input/Output Screens Designs
   4.8 Coding
5. Result and Discussion
   5.1 Overview of Results
   5.2 Program Testing
   5.3 Module Testing
   5.4 Integration Testing
   5.5 System Testing
   5.6 Input/Output Screens and Reports
6. Conclusions and Future Scope
   6.1 Conclusion
   6.2 Limitations
   6.3 Future Scope
7. Literature Cited
8. References
9. Appendices
   9.1 List of Publications
   9.2 Plagiarism Report
   9.3 List of Participation
   9.4 Company Certificate
   9.5 Any Other (Tools/Data/Code Listing etc)
   9.6 Author Note

---

# Chapter 1: INTRODUCTION

## 1.1 Overview

In the digital age, online shoppers often visit multiple websites to compare prices for the same product. This process is time-consuming and inefficient. The **Price Comparison Tool** aims to solve this problem by aggregating price data from multiple e-commerce platforms and displaying it in a single interface. This thesis documents the development of this tool using a **Django** backend and a **React** frontend.

The project includes:
- Secure user signup, login, and email verification,
- Product search by name or model number,
- Price aggregation from multiple sources,
- Wishlist functionality,
- Dashboard analytics for users,
- Responsive user interface.

Architecture is modular to allow future extension, such as price alert notifications and more data sources.

## 1.2 Problem Statement

Consumers face several challenges while shopping online:
- Spending excessive time comparing prices across multiple websites.
- Difficulty identifying the most competitive offer for a product.
- Lack of a single interface that aggregates product details, availability, and pricing.
- No simple way to save preferred items or monitor price changes.

The project addresses these issues by providing:
- a centralized comparison interface,
- authenticated user access,
- wishlist management,
- product analytics and price trend visibility.

## 1.3 Objectives of the Study

The main objectives of this project are:
- Develop a web application to compare product prices from multiple online stores.
- Implement secure user authentication with email verification.
- Provide a dashboard for user statistics and profile management.
- Enable wishlist creation and price target alerts.
- Ensure responsive and intuitive design for desktop and mobile use.

## 1.4 Scope of the Project

The project scope includes:
- Backend API with user authentication, verify email, product comparison, wishlist, and profile management.
- Frontend web app with search, comparison results, dashboard, wishlist, login, and signup.
- Data model to support products, price listings, wishlists, and user profiles.
- Deployment readiness for development and potential production environments.

Excluded from current scope:
- fully automated third-party web scraping,
- machine learning-based recommendations,
- mobile-native application.

## 1.5 Methodology

This project used an iterative development methodology:
- Requirement analysis
- System design
- Implementation
- Testing
- Documentation

Each phase built on the previous one. The application was developed using rapid prototyping, with frequent validation against user requirements.

## 1.6 Tools and Technologies

### Software
- Python 3.x
- Django
- Django REST Framework
- React
- Vite
- Bootstrap
- Axios
- SQLite
- Git
- Node.js
- npm

### Hardware
- Development laptop/desktop
- Minimum: 8 GB RAM, modern CPU, 20 GB free disk space
- Internet connection for dependencies, email testing, and research

---

# Chapter 2: LITERATURE SURVEY & REVIEW

## 2.1 Overview

Price comparison solutions combine domains from e-commerce, data mining, information retrieval, and UI/UX design. Existing research examines both the technical and consumer-facing aspects of comparison shopping.

## 2.2 Review of Literature

### 2.2.1 Price Comparison and E-Commerce
Turban and Outland (2018) explore e-commerce management and emphasize that comparison shopping agents reduce consumer search costs and improve pricing transparency.

> Turban, E., & Outland, J. (2018). *Electronic Commerce 2018: A Managerial Perspective* (15th ed.). Pearson.

Laudon and Traver (2018) analyze e-commerce systems and highlight trust, security, and usability as critical success factors.

> Laudon, K. C., & Traver, C. G. (2018). *E-commerce 2018: Business, Technology, Society* (14th ed.). Pearson.

### 2.2.2 Web Data Mining
Liu (2007) provides techniques for extracting and preprocessing data from web sources, essential for normalizing product information across different e-commerce websites.

> Liu, B. (2007). *Web Data Mining: Exploring Hyperlinks, Contents, and Usage Data* (2nd ed.). Springer.

### 2.2.3 Data Mining Techniques
Han, Kamber, and Pei (2011) discuss data mining methods useful for analyzing price trends and extracting actionable insight from price history and listings.

> Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.

### 2.2.4 Information Retrieval
Baeza-Yates and Ribeiro-Neto (2011) investigate query processing and retrieval systems, which inform search accuracy for product model and name matching.

> Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern Information Retrieval: The Concepts and Technology behind Search* (2nd ed.). Addison-Wesley.

### 2.2.5 Recommender Systems
Ricci et al. (2015) outline recommender system architectures that can enhance personalization and user engagement in price comparison tools.

> Ricci, F., Rokach, L., Shapira, B., & Kantor, P. B. (2015). *Recommender Systems Handbook* (2nd ed.). Springer.

## 2.3 Research Gap

Existing literature often treats price comparison, search, or personalization separately. This project fills a gap by combining:
- secure authentication,
- product comparison,
- wishlist management,
- dashboard analytics,
- responsive web interface.

The thesis contributes a cohesive implementation with practical, user-centered features.

---

# Chapter 3: WORKDONE – SYSTEM ANALYSIS

## 3.1 Methodology

This chapter describes the methodologies used:
- Requirement gathering from stakeholder expectations,
- Use case analysis,
- Modular planning,
- Iterative development.

## 3.2 Identification of Need

The need arises from:
- user difficulty comparing prices manually,
- demand for a central product search interface,
- convenience of saved product lists,
- desire for authenticated tracking and personalized data.

## 3.3 Preliminary Investigation

Initial research included:
- reviewing existing comparison platforms,
- determining available technology stacks,
- identifying functional and non-functional requirements,
- choosing Django + React.

## 3.4 Feasibility Study

### Technical Feasibility
- Backend: Django REST Framework, token authentication, email verification.
- Frontend: React, Vite, Bootstrap.
- Database: SQLite for development, PostgreSQL for production.

### Economic Feasibility
- Open-source tools minimize cost.
- Development time acceptable within project schedule.

### Operational Feasibility
- UI is user-friendly.
- System is easy to deploy and maintain.
- Future enhancements possible with modular architecture.

### Legal Feasibility
- No unauthorized scraping of protected sources.
- Data is managed within project scope.

## 3.5 Project Planning

Project phases:
- Requirement analysis and design
- Backend implementation
- Frontend implementation
- Testing and validation
- Documentation and evaluation

A Gantt chart or timeline can be included in the final document.

## 3.6 Software/Hardware Requirement

### Software Requirements
- Python, Django, REST framework
- Node.js, npm, React
- Database management tools
- Email server configuration for verification

### Hardware Requirements
- Development PC with minimum 8 GB RAM
- 500 GB disk space
- Internet access

---

# Chapter 4: WORKDONE – SYSTEM DESIGN

## 4.1 Modularization Details

The system is divided into the following modules:

### 4.1.1 Authentication Module
- Signup
- Login
- Email verification
- Logout

### 4.1.2 Product Comparison Module
- Search by model or name
- Aggregate multi-platform price listings
- Show buy links

### 4.1.3 Wishlist Module
- Add products to wishlist
- Store target price
- Notify price drops (future scope)

### 4.1.4 Dashboard Module
- Display wishlist count
- Display compared product count
- Profile editing

### 4.1.5 Data Ingestion Module
- Product listing management
- Price history records
- Adapter pipeline for platform-specific price updates

## 4.2 Database Design

### Entity-Relationship Diagram
Figure 1: Placeholder for ER diagram showing:
- User
- AccountProfile
- EmailVerificationToken
- Product
- ProductPrice
- ProductListing
- PriceHistory
- WishlistItem

### Tables
- `auth_user`
- `apps_core_accountprofile`
- `apps_core_emailverificationtoken`
- `apps_core_product`
- `apps_core_productprice`
- `apps_core_productlisting`
- `apps_core_pricehistory`
- `apps_core_wishlistitem`

## 4.3 Data Dictionary

### Product
- `id`: Unique identifier
- `name`: Product name
- `model_number`: Unique model number
- `brand`: Brand name
- `image_url`: Product image
- `category`: Product category

### ProductPrice
- `product_id`
- `source`
- `price`
- `buy_url`
- `in_stock`
- `fetched_at`

### WishlistItem
- `user_id`
- `product_id`
- `target_price`
- `notify_on_drop`
- `created_at`

### ProductListing
- `product_id`
- `platform`
- `platform_product_id`
- `title`
- `buy_url`
- `current_price`
- `in_stock`
- `fetched_at`
- `last_error`

### PriceHistory
- `listing_id`
- `price`
- `in_stock`
- `captured_at`

### AccountProfile
- `user_id`
- `email_verified`

### EmailVerificationToken
- `user_id`
- `token`
- `created_at`

## 4.4 Data Flow Diagram

### Level 0 DFD
Figure 2: Placeholder for DFD showing:
- User interacts with frontend
- Frontend requests backend APIs
- Backend queries database and returns JSON

### Level 1 DFD
Figure 3: Placeholder for detailed DFD including:
- Signup/login flow
- Product compare flow
- Wishlist flow
- Dashboard flow

## 4.5 System Flowchart

Figure 4: Placeholder for system flowchart:
- Start
- Login/Signup
- Search product
- Display results
- Add to wishlist
- View dashboard
- Logout
- End

## 4.6 Program Flowcharts

### Signup Flowchart
Figure 5: Placeholder for signup and verification process.

### Login Flowchart
Figure 6: Placeholder for login and token generation.

### Product Search Flowchart
Figure 7: Placeholder for query input and result display.

### Wishlist Flowchart
Figure 8: Placeholder for wishlist add/remove logic.

### Profile Update Flowchart
Figure 9: Placeholder for profile edit and save flow.

## 4.7 Input/Output Screens Designs

### Login Page
- Username/email field
- Password field
- Login button
- Link to signup

### Signup Page
- First name, last name, username
- Email, password, confirm password
- Validation messages

### Compare Page
- Search box
- Price comparison cards
- Platform table
- Add to wishlist button

### Wishlist Page
- Wishlist items list
- Product details and target price
- Remove action

### Dashboard Page
- Welcome message
- Wishlist and compared product counts
- Profile form
- Password update section

## 4.8 Coding

### Backend Implementation
- `apps/core/views.py`
  - `SignupView`
  - `login_view`
  - `logout_view`
  - `verify_email_view`
  - `compare_search_view`
  - `dashboard_view`
  - `UserProfileView`
  - `WishlistViewSet`

- `apps/core/serializers.py`
  - `SignupSerializer`
  - `ProductSerializer`
  - `ProductPriceSerializer`
  - `WishlistItemSerializer`
  - `UserProfileSerializer`

- `apps/core/models.py`
  - Product and price models
  - Wishlist and profile models

### Frontend Implementation
- `src/App.jsx`
  - Routing and navigation
  - PrivateRoute
- `src/api.js`
  - Axios base URL and token interceptor
- `src/pages/SignupPage.jsx`
  - Form validation and signup flow
- `src/pages/LoginPage.jsx`
  - Login and redirect to compare page
- `src/pages/ComparePage.jsx`
  - Search, results rendering, wishlist integration
- `src/pages/DashboardPage.jsx`
  - Dashboard cards and profile edit form
- `src/pages/WishlistPage.jsx`
  - Wishlist display and removal

---

# Chapter 5: RESULT AND DISCUSSION

## 5.1 Overview of Results

The system successfully:
- enables user registration with email verification,
- provides product comparison,
- supports wishlist management,
- displays dashboard metrics.

## 5.2 Program Testing

### Functional Tests
- Signup valid and invalid inputs
- Email verification path
- Login and logout behavior
- Search queries return results
- Wishlist add/remove actions
- Profile update with name and password change

### Performance Tests
- Response time for API endpoints
- Page load time for compare and dashboard
- Scalability of product search results

## 5.3 Module Testing

### Authentication Module
- Verified token issuance and email verification logic
- Checked error messages for invalid credentials

### Product Comparison Module
- Verified search by model and name
- Confirmed price data aggregation

### Wishlist Module
- Verified adding and listing wishlist items
- Checked uniqueness constraint per user-product

### Dashboard Module
- Verified user statistic retrieval
- Confirmed profile update persistence

## 5.4 Integration Testing

Integrated tests showed the complete flow:
- Signup → verify email → login → search → add wishlist → view dashboard.

## 5.5 System Testing

System tests covered:
- Browser compatibility
- API endpoint accessibility
- Authentication and authorization checks
- Form validation

## 5.6 Input/Output Screens and Reports

Screenshots and UI reports should include:
- login page,
- signup page,
- compare page,
- wishlist page,
- dashboard page.

Reports demonstrate the system’s usability.

---

# Chapter 6: CONCLUSIONS AND FUTURE SCOPE

## 6.1 Conclusion

This project developed a functional price comparison tool with:
- secure authentication,
- email verification,
- multi-platform price comparison,
- wishlist and dashboard functionality.

It demonstrates how a Django + React stack can deliver a full-featured e-commerce support application.

## 6.2 Limitations

- Current data sources are limited.
- Live price updates are manually triggered or scheduled.
- Price alert notifications are planned but not fully implemented.

## 6.3 Future Scope

Potential enhancements:
- Add more marketplaces and product categories.
- Implement real-time scraping or API integration.
- Add price drop alerts and email notifications.
- Build charts for price history.
- Deploy on cloud platforms with HTTPS and PostgreSQL.
- Add admin panel for product and listing management.

---

# Chapter 7: LITERATURE CITED

Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern Information Retrieval: The Concepts and Technology behind Search* (2nd ed.). Addison-Wesley.

Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.

Laudon, K. C., & Traver, C. G. (2018). *E-commerce 2018: Business, Technology, Society* (14th ed.). Pearson.

Liu, B. (2007). *Web Data Mining: Exploring Hyperlinks, Contents, and Usage Data* (2nd ed.). Springer.

Ricci, F., Rokach, L., Shapira, B., & Kantor, P. B. (2015). *Recommender Systems Handbook* (2nd ed.). Springer.

Turban, E., & Outland, J. (2018). *Electronic Commerce 2018: A Managerial Perspective* (15th ed.). Pearson.

---

# Chapter 8: REFERENCES

- Django Software Foundation. (2024). Django.
- React. (2024). React documentation.
- Vite. (2024). Vite documentation.
- Bootstrap. (2024). Bootstrap documentation.
- Axios. (2024). Axios documentation.

---

# Chapter 9: APPENDICES

## 9.1 List of Publications

- None / To be filled if applicable.

## 9.2 Plagiarism Report

- Include Turnitin report summary and percentage.

## 9.3 List of Participation

- Workshops, seminars, or competitions attended during the project.

## 9.4 Company Certificate

- Internship/industrial training certifications.

## 9.5 Any Other (Tools/Data/Code Listing etc)

- Tools used: Git, VS Code, Python, Node.js, Django, React.
- Data sources: product listing seed data, platform price data.
- Code listing: major modules and scripts.

## 9.6 Author Note

- Personal reflection on project challenges, learning outcomes, and future improvements.

---

## Diagram Placeholders

- **Figure 1:** System Architecture Diagram
- **Figure 2:** Data Flow Diagram (Level 0)
- **Figure 3:** Data Flow Diagram (Level 1)
- **Figure 4:** System Flowchart
- **Figure 5:** Signup Flowchart
- **Figure 6:** Login Flowchart
- **Figure 7:** Product Search Flowchart
- **Figure 8:** Wishlist Flowchart
- **Figure 9:** Profile Update Flowchart
