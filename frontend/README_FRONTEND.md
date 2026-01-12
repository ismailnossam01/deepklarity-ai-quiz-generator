# Frontend Setup Guide

## Prerequisites

1. **Node.js 16+** installed
2. **Backend API** running on http://localhost:8000

## Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install:
- React 18
- Vite (build tool)
- Tailwind CSS
- Axios (for API calls)

## Step 2: Configure Environment

The `.env` file should already have:
```env
VITE_API_URL=http://localhost:8000
```

If your backend runs on a different port, update this.

## Step 3: Run Development Server

```bash
npm run dev
```

The app will open automatically at: **http://localhost:5173**

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── LoadingSpinner.jsx
│   │   ├── QuizCard.jsx
│   │   ├── QuizList.jsx
│   │   ├── HistoryTable.jsx
│   │   └── QuizModal.jsx
│   ├── pages/              # Main page components
│   │   ├── GenerateQuiz.jsx  # Tab 1
│   │   └── History.jsx        # Tab 2
│   ├── App.jsx             # Main app with tabs
│   ├── api.js              # API service layer
│   ├── main.jsx            # React entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
└── tailwind.config.js      # Tailwind CSS config
```

## Features

### Tab 1: Generate Quiz
- Enter Wikipedia URL
- Click "Generate Quiz"
- View quiz with answers OR take quiz interactively
- See key entities, sections, and related topics

### Tab 2: History
- View all previously generated quizzes
- Click "View Details" to open modal
- See quiz statistics

## Building for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized production files.

## Preview Production Build

```bash
npm run preview
```

## Troubleshooting

### Issue: White screen / App not loading
**Solution:** Check browser console for errors. Make sure backend is running.

### Issue: "Backend Disconnected" message
**Solution:** 
1. Check backend is running: http://localhost:8000
2. Verify VITE_API_URL in .env matches backend URL
3. Check CORS settings in backend

### Issue: Tailwind styles not working
**Solution:** 
1. Delete `node_modules` folder
2. Run `npm install` again
3. Restart dev server

### Issue: API calls failing
**Solution:**
1. Check Network tab in browser DevTools
2. Verify backend endpoints are working: http://localhost:8000/docs
3. Check for CORS errors

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool (faster than Create React App)
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

