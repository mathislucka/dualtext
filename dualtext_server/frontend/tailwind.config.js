module.exports = {
  purge: [
    './src/**/*.vue',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
    colors: {
        blue: {
            '100': '#e6f3fe',
            '200': '#b4dafd',
            '300': '#82c2fc',
            '400': '#50aafb',
            '500': '#1e91fa',
            '600': '#0578e1',
            '700': '#045daf',
            '800': '#03437d',
            '900': '#02284b',
            '1000': '#010d19'
        },
	    grey: {
		    '100': '#f2f2f2',
		    '200': '#d9d9d9',
		    '300': '#bfbfbf',
		    '400': '#a6a6a6',
		    '500': '#8c8c8c',
		    '600': '#737373',
		    '700': '#595959',
		    '800': '#404040',
		    '900': '#262626',
		    '1000': '#0d0d0d'
	    },
	    red: {
		    '100': '#fdebe8',
		    '200': '#f8c2ba',
		    '300': '#f3998b',
		    '400': '#ef715d',
		    '500': '#ea482f',
		    '600': '#d02f15',
		    '700': '#a22410',
		    '800': '#741a0c',
		    '900': '#451007',
		    '1000': '#170502'
	    },
	    green: {
		    '100': '#eff8ec',
		    '200': '#d0eac7',
		    '300': '#b0dca2',
		    '400': '#91ce7d',
		    '500': '#71c058',
		    '600': '#57a73f',
		    '700': '#448231',
		    '800': '#315d23',
		    '900': '#1d3815',
		    '1000': '#0a1307'
	    },
	    teal: {
		    '100': '#eafaf7',
		    '200': '#c0f1e8',
		    '300': '#97e8d8',
		    '400': '#6ddec9',
		    '500': '#43d5b9',
		    '600': '#2abca0',
		    '700': '#21927c',
		    '800': '#176859',
		    '900': '#0e3f35',
		    '1000': '#051512'
        },
        white: {
            'DEFAULT': '#ffffff'
        }
    }
  },
  variants: {
    extend: {},
  },
  plugins: [],
}