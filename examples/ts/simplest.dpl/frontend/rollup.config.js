import typescript from '@rollup/plugin-typescript';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import replace from 'rollup-plugin-replace';

// `npm run build` -> `production` is true
// `npm run dev` -> `production` is false
const production = !process.env.ROLLUP_WATCH;

export default {
    input: 'index.tsx',
    output: {
	file: 'public/bundle.js',
	format: 'iife', // immediately-invoked function expression — suitable for <script> tags
	sourcemap: true,
    },
    plugins: [
	typescript(),
	replace({'process.env.NODE_ENV': JSON.stringify('production'),}), // to fix react imports
	resolve(), // tells Rollup how to find date-fns in node_modules
	commonjs({namedExports: {		
	    'node_modules/react/index.js': ['createElement', 'Component'],
	    'node_modules/react-dom/index.js': ['render']
	    }}), // converts date-fns to ES modules
	//production && terser() // minify, but only in production
    ]
};
