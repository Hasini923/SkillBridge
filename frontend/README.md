# SkillBridge Frontend

React-based frontend for SkillBridge - AI Career & Skill Gap Advisor

## 🚀 Quick Start

### Prerequisites
- Node.js 14+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 📁 File Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.jsx             # Main component
│   ├── App.css             # App styling
│   ├── index.jsx           # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies
└── .gitignore             # Git ignore rules
```

## 🔧 Configuration

### Backend URL

By default, the app connects to `http://localhost:5000`

To change the backend URL, update in `App.jsx`:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

Or set environment variable:

```bash
REACT_APP_API_URL=https://your-backend-url.com npm start
```

## 📦 Dependencies

- **react** - UI library
- **react-dom** - React rendering
- **lucide-react** - Icons library

## ✨ Features

- 📄 PDF resume upload
- 🎯 Target role input
- 🔍 AI-powered skill analysis
- 📊 Match score calculation
- 🛣️ Personalized learning roadmap
- 💪 Strength identification
- ⬇️ Download roadmap as text file

## 🔌 API Integration

### Endpoints Used

1. **POST /upload-resume** - Upload and extract resume text
2. **POST /analyze-resume** - Analyze skills and generate roadmap

See `App.jsx` for implementation details.

## 🎨 Styling

Uses custom CSS with:
- Responsive grid layouts
- Smooth animations
- Tailwind-inspired utility classes
- Mobile-friendly design

## 🚀 Building for Production

```bash
npm run build
```

This creates an optimized build in the `build/` folder.

### Deploy to Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
# Connect GitHub repo and deploy automatically
# Or drag and drop build folder
```

## 🐛 Troubleshooting

### CORS Error
Make sure backend is running on `http://localhost:5000`

### Blank Page
Check browser console for errors. Make sure all dependencies are installed.

### API Not Responding
1. Check backend is running: `python app.py`
2. Verify correct API URL in `App.jsx`
3. Check network tab in browser DevTools

## 📝 Notes

- Resume must be PDF format
- Target role should be specific (e.g., "Machine Learning Engineer")
- Analysis takes 30-60 seconds due to Gemini API calls
- Results are NOT saved (frontend only)

## 🤝 Support

For issues or questions, check the main SkillBridge README or contact the team.