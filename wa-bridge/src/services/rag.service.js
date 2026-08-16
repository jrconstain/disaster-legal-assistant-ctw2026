const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');
const Fuse = require('fuse.js');

class RagService {
    constructor() {
        this.knowledgeChunks = [];
        this.fuse = null;
        this.isReady = false;
        this.docsPath = path.join(__dirname, '..', 'Documentacion');
    }

    async init() {
        console.log('Inicializando Base de Conocimientos RAG...');
        try {
            const files = fs.readdirSync(this.docsPath).filter(file => file.endsWith('.pdf') || file.endsWith('.txt'));
            
            for (const file of files) {
                const filePath = path.join(this.docsPath, file);
                let text = '';
                
                try {
                    if (file.endsWith('.pdf')) {
                        const dataBuffer = fs.readFileSync(filePath);
                        const data = await pdfParse(dataBuffer);
                        text = data.text || '';
                    } else if (file.endsWith('.txt')) {
                        text = fs.readFileSync(filePath, 'utf8');
                    }
                    
                    // Estrategia de chunking: separar por saltos de línea dobles y filtrar párrafos cortos
                    const chunks = text.split(/\n\s*\n/).filter(c => c.trim().length > 50);
                    
                    chunks.forEach((chunk, index) => {
                        this.knowledgeChunks.push({
                            source: file,
                            chunkIndex: index,
                            content: chunk.trim()
                        });
                    });
                    
                } catch (pdfErr) {
                    console.error(`Error procesando archivo ${file}:`, pdfErr);
                }
            }

            console.log(`Base de conocimientos cargada con ${this.knowledgeChunks.length} párrafos.`);

            // Inicializar Fuse.js para búsqueda difusa (fuzzy search)
            const options = {
                includeScore: true,
                threshold: 0.6, // Ajuste para requerir cierta coincidencia
                keys: ['content'],
                ignoreLocation: true,
                minMatchCharLength: 5
            };
            
            this.fuse = new Fuse(this.knowledgeChunks, options);
            this.isReady = true;

        } catch (err) {
            console.error('Error inicializando RAG Service:', err);
        }
    }

    searchKnowledge(query, topK = 3) {
        if (!this.isReady || !this.fuse) {
            return [];
        }

        // Ignoramos mensajes muy cortos como "hola", "si"
        if (!query || query.length < 10) {
            return [];
        }

        const results = this.fuse.search(query);
        // Retornamos los mejores topK
        return results
            .slice(0, topK)
            .map(res => res.item);
    }
}

module.exports = new RagService();
