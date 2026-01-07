import * as pdfjsLib from 'pdfjs-dist';

// Set up the worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

/**
 * Extract text from PDF file
 * @param {File} file - PDF file object
 * @returns {Promise<string>} - Extracted text
 */
export const extractTextFromPDF = async (file) => {
  try {
    console.log('📄 Starting PDF extraction...');
    
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    
    console.log(`📖 PDF loaded with ${pdf.numPages} pages`);
    
    let fullText = '';
    
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      try {
        const page = await pdf.getPage(pageNum);
        const textContent = await page.getTextContent();
        const pageText = textContent.items
          .map(item => item.str)
          .join(' ');
        
        fullText += pageText + '\n';
        console.log(`✅ Extracted page ${pageNum}/${pdf.numPages}`);
      } catch (pageError) {
        console.warn(`⚠️ Error extracting page ${pageNum}:`, pageError);
        continue;
      }
    }
    
    console.log(`✅ Total text extracted: ${fullText.length} characters`);
    return fullText;
  } catch (error) {
    console.error('❌ PDF extraction failed:', error);
    throw new Error(`Failed to extract text from PDF: ${error.message}`);
  }
};