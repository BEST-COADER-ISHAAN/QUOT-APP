# QUOT-APP

1. Purpose of the Application
The application is designed for local use to automate the process of generating professional quotations, managing customers, and keeping track of products. It eliminates the need for repetitive data entry, ensures consistency, and supports features like PDFs and product tracking.

2. Key Features
Customer Management:

Add, edit, or delete customer details.
Store customer information like name, address, phone number, and email.
Product Management:

Add, edit, or delete product details.
Store information like product name, size (in mm), surface type, rate per square foot, rate per box, image, links (360° view and website), and additional details.
Quotation Generation:

Automatically generate quotation numbers.
Generate PDFs with a structured layout:
First Page: Contains customer details and a table summarizing all products in the quotation.
Subsequent Pages: Each product has a dedicated page with:
Left: Space for the product image.
Right: Product details (name, rate per box, quantity, links, and more).
Dynamic pagination for any number of products.
Home Page Dashboard:

Charts and graphs showing product trends (e.g., most sold products).
Quick access to view or download recent quotations.
PDF Management:

Save all generated PDFs in a dedicated folder for easy retrieval.
PDFs include total amounts in numeric and word formats.
Additional Features:

Search/Filter: Quickly locate customers or products.
Customization Options: Add your logo, header, and footer to the quotation format.
Dark Mode: Toggle between light and dark themes.
Responsive Design: User interface adjusts to different screen sizes.
Progress Indicators: Visualize steps completed when creating a quotation.
3. Folder Structure
graphql
Copy code
automatic-quotation-generator/
├── app/
│   ├── database/
│   │   ├── customers.db        # Stores customer data
│   │   ├── products.db         # Stores product data
│   │   └── quotations.db       # Stores quotation records
│   ├── pdfs/                   # Stores generated PDFs
│   ├── static/
│   │   ├── images/             # Stores product images
│   │   └── css/
│   │       └── style.css       # Contains CSS for styling
│   ├── templates/              # HTML files for UI
│   │   ├── base.html
│   │   ├── home.html           # Dashboard page
│   │   ├── add_customer.html   # Add customer page
│   │   ├── add_product.html    # Add product page
│   │   └── view_quotation.html # View/download quotations
│   ├── main.py                 # Main Flask app logic
│   ├── quotation_generator.py  # PDF generation logic
│   └── static_content.py       # Manage static resources
4. Detailed Workflow
Step 1: Manage Customers
Use the Add Customer page to input customer details.
Stored in customers.db.
Step 2: Manage Products
Use the Add Product page to input product details, including:
Product name, size, surface, rate per square foot, rate per box, quantity, image, 360° view link, and website link.
Stored in products.db.
Step 3: Generate Quotation
Choose the customer and select products from the database.
Input quantities for each product in the quotation.
Automatically calculate totals and amounts in words.
Generate and save the PDF.
Step 4: View Dashboard
See top-selling products via charts.
Access and download recent quotations.
5. Detailed Description of Generated Quotation PDF
First Page:

Customer details: Name, address, phone number, etc.
A table summarizing products with the following columns:
Product Name: Name of the product.
Size (mm): Dimensions of the product.
Surface: Type of surface (e.g., Glossy, Matte).
Rate/sq. ft: Price per square foot (informational only).
Rate per Box: Price per box.
Quantity: Number of boxes purchased.
Total: Quantity × Rate per Box.
Displays Total Amount and Amount in Words.
Subsequent Pages:

Each product has its own page:
Left: Space for product image.
Right: Product details:
Product name.
Rate per box.
Quantity.
Links to 360° view and website.
Additional details.
6. Features to Add in the Future
Product Bundles: Add multiple products as a package.
Multi-Currency Support: Generate quotations in different currencies.
Tax Calculations: Add applicable taxes and show tax breakdown.
Invoice Integration: Extend the app to generate invoices based on quotations.
Reminders: Notify you when quotations require follow-up.
Data Export: Export customer and product data to Excel or CSV.
7. Modules and Tools
Backend:
Flask: Build the application and serve web pages.
SQLite: Manage databases for customers, products, and quotations.
PDF Generation:
FPDF: Create professional PDF documents.
num2words: Convert numeric totals into words.
Frontend:
HTML, CSS (via style.css), and JavaScript for a responsive UI.
Visualization:
Matplotlib or Chart.js: Display charts for product trends.
