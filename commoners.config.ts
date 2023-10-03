const defineConfig = (o) => o 

export default defineConfig({
    
    icon: './src/assets/commoners.png', 

    services: {

        python: {
            src: './src/services/python/main.py',
            port: 2020,
            publish: {
                build: 'python -m PyInstaller --name test --onedir --clean ./src/services/python/main.py --distpath ./dist/services/python',
                local: './dist/services/python/test/test'
            }
        }
    }
})