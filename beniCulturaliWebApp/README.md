# BeniCulturaliWebApp Frontend

Welcome to the frontend of the BeniCulturaliWebApp!

---

## What’s Inside?

- **React**: The app is built with React, a popular framework for making interactive web interfaces.
- **Vite**: Vite is used as our development server and build tool. It’s super fast and makes development smooth.
- **JavaScript**: All the main logic is written in JS, with modern syntax and conventions.
- **CSS**: Custom styles keep the layout clean and responsive.
- **ESLint**: Code linting helps catch mistakes before they become bugs.

---

## Main App Features

- **Homepage Structure**:  
  - **Header** and **Footer** for navigation and info.
  - **Hero Section** – a big welcoming banner with a background image and catchy title.
  - **Search** – Type in keywords to explore cultural artifacts (powered by a custom search hook).
  - **Category Tiles** – (if enabled) lets users browse by cultural category.

- **Smart Search**:  
  - Type in what you’re looking for, and the app waits a moment before searching—so it doesn’t hit the server with every keystroke.
  - Handles errors and loading states gracefully.
  - Aborts old searches if you type something new right away (no wasted requests!).

- **Styling**:  
  - The app is responsive and uses modern CSS practices for layout and typography.
  - Accessible color choices and readable fonts.

---

## How to Run the App

1. Open your terminal and go to the `BeniCulturaliWebApp` folder.
2. Install dependencies:  
   ```bash
   npm install
   ```
3. Start the development server:  
   ```bash
   npm run dev
   ```
4. Visit [http://localhost:5174](http://localhost:5174) in your browser.

---

## Tips & Suggestions

- **Component Docs**: Briefly comment your components and hooks—future you will thank you!
- **API Utility**: The API helpers are well-abstracted, but add usage notes if you extend them.
- **Accessibility**: Consider adding ARIA attributes and more semantic HTML for improved usability.

---

## More Info

- See the [BeniCulturaliWebApp folder on GitHub](https://github.com/Sal-Omon/Sal-Omon.github.io/tree/main/beniCulturaliWebApp) for all files.

