/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html", "./static/**/*.js"],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: "#2d7fd2",
                cta: "#FF6B35",
                "bg-dark": "#080E18",
                surface: "#0D1721",
                border: "#1e293b",
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/container-queries'),
    ],
}
