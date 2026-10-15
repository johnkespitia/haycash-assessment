import { playwright } from '@vitest/browser-playwright';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	test: {
		projects: [
			{
				extends: true,
				test: {
					name: 'unit',
					include: ['src/**/*.{test,spec}.{js,ts}'],
					exclude: ['src/**/*.svelte.{test,spec}.{js,ts}'],
					environment: 'node'
				}
			},
			{
				extends: true,
				test: {
					name: 'component',
					include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
					browser: {
						enabled: true,
						provider: playwright(),
						instances: [{ browser: 'chromium', headless: true }]
					}
				}
			}
		]
	}
});
