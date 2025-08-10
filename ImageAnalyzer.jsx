import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { Upload, Camera, Loader2, AlertTriangle, Info, X } from 'lucide-react'
import '../App.css'

const ImageAnalyzer = ({ language }) => {
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const text = {
    en: {
      title: 'Skin Condition Analysis',
      description: 'Upload a clear image of the skin area you want to analyze. Our AI will examine it for potential conditions.',
      uploadButton: 'Upload Image',
      takePhoto: 'Take Photo',
      analyze: 'Analyze Image',
      analyzing: 'Analyzing Image...',
      results: 'Analysis Results',
      imageQuality: 'Image Quality Assessment',
      skinCondition: 'Skin Condition Analysis',
      recommendations: 'Recommendations',
      riskAssessment: 'Risk Assessment',
      confidence: 'Confidence Level',
      disclaimer: 'Medical Disclaimer',
      disclaimerText: 'This analysis is for informational purposes only and does not replace professional medical advice. Please consult with a dermatologist for proper diagnosis and treatment.',
      noImage: 'Please upload an image to analyze.',
      analysisError: 'Failed to analyze image. Please try again.',
      invalidFile: 'Please upload a valid image file (JPG, PNG, or WebP).',
      removeImage: 'Remove Image',
      quality: 'Quality',
      condition: 'Condition',
      probability: 'Probability',
      risk: 'Risk Level',
      uploadInstructions: 'Drag and drop an image here, or click to select',
      supportedFormats: 'Supported formats: JPG, PNG, WebP (max 10MB)'
    },
    ar: {
      title: 'تحليل الحالات الجلدية',
      description: 'ارفع صورة واضحة لمنطقة الجلد التي تريد تحليلها. سيقوم الذكاء الاصطناعي بفحصها للحالات المحتملة.',
      uploadButton: 'رفع صورة',
      takePhoto: 'التقاط صورة',
      analyze: 'تحليل الصورة',
      analyzing: 'جاري تحليل الصورة...',
      results: 'نتائج التحليل',
      imageQuality: 'تقييم جودة الصورة',
      skinCondition: 'تحليل الحالة الجلدية',
      recommendations: 'التوصيات',
      riskAssessment: 'تقييم المخاطر',
      confidence: 'مستوى الثقة',
      disclaimer: 'إخلاء المسؤولية الطبية',
      disclaimerText: 'هذا التحليل لأغراض إعلامية فقط ولا يحل محل المشورة الطبية المهنية. يرجى استشارة طبيب الأمراض الجلدية للحصول على التشخيص والعلاج المناسب.',
      noImage: 'يرجى رفع صورة للتحليل.',
      analysisError: 'فشل في تحليل الصورة. يرجى المحاولة مرة أخرى.',
      invalidFile: 'يرجى رفع ملف صورة صالح (JPG, PNG, أو WebP).',
      removeImage: 'إزالة الصورة',
      quality: 'الجودة',
      condition: 'الحالة',
      probability: 'الاحتمالية',
      risk: 'مستوى المخاطر',
      uploadInstructions: 'اسحب وأفلت صورة هنا، أو انقر للاختيار',
      supportedFormats: 'الصيغ المدعومة: JPG, PNG, WebP (حد أقصى 10 ميجابايت)'
    }
  }

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleFile = (file) => {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if (!validTypes.includes(file.type)) {
      setError(text[language].invalidFile)
      return
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB')
      return
    }

    setError(null)
    setSelectedImage(file)
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setImagePreview(e.target.result)
    }
    reader.readAsDataURL(file)
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  const removeImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    setResults(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const analyzeImage = async () => {
    if (!selectedImage) {
      setError(text[language].noImage)
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setResults(null)

    try {
      // Mock analysis - replace with actual backend call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock results
      const mockResults = {
        imageQuality: {
          overall: 'good',
          sharpness: 85,
          lighting: 78,
          resolution: 92
        },
        skinConditionAnalysis: {
          primaryCondition: 'Acne Vulgaris',
          probability: 0.78,
          severity: 'moderate',
          affectedArea: 'facial_region'
        },
        recommendations: [
          {
            type: 'immediate',
            action: language === 'en' 
              ? 'Keep the affected area clean with gentle cleansing'
              : 'حافظ على نظافة المنطقة المصابة بالتنظيف اللطيف',
            priority: 'high'
          },
          {
            type: 'lifestyle',
            action: language === 'en'
              ? 'Avoid touching or picking at the affected area'
              : 'تجنب لمس أو حك المنطقة المصابة',
            priority: 'medium'
          },
          {
            type: 'medical',
            action: language === 'en'
              ? 'Consider consulting a dermatologist for treatment options'
              : 'فكر في استشارة طبيب الأمراض الجلدية لخيارات العلاج',
            priority: 'high'
          }
        ],
        riskAssessment: {
          level: 'low',
          factors: ['No signs of infection', 'Localized condition'],
          monitoring: 'Monitor for changes over 1-2 weeks'
        },
        confidenceScore: 0.82
      }

      setResults(mockResults)
    } catch (err) {
      setError(text[language].analysisError)
      console.error('Analysis error:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getQualityColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getRiskColor = (level) => {
    switch (level) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200'
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Upload Section */}
      <Card>
        <CardHeader>
          <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
            {text[language].title}
          </CardTitle>
          <CardDescription className={language === 'ar' ? 'text-right' : 'text-left'}>
            {text[language].description}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!imagePreview ? (
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors cursor-pointer"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg font-medium text-gray-900 mb-2">
                {text[language].uploadInstructions}
              </p>
              <p className="text-sm text-gray-500">
                {text[language].supportedFormats}
              </p>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative">
                <img
                  src={imagePreview}
                  alt="Selected for analysis"
                  className="w-full max-w-md mx-auto rounded-lg shadow-lg"
                />
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={removeImage}
                  className="absolute top-2 right-2"
                >
                  <X className="h-4 w-4" />
                  {text[language].removeImage}
                </Button>
              </div>
            </div>
          )}

          {error && (
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="flex gap-2">
            <Button
              onClick={() => fileInputRef.current?.click()}
              variant="outline"
              className="flex-1"
            >
              <Upload className="mr-2 h-4 w-4" />
              {text[language].uploadButton}
            </Button>
            <Button
              onClick={analyzeImage}
              disabled={isAnalyzing || !selectedImage}
              className="flex-1"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  {text[language].analyzing}
                </>
              ) : (
                <>
                  <Camera className="mr-2 h-4 w-4" />
                  {text[language].analyze}
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results Section */}
      {results && (
        <div className="space-y-6">
          {/* Medical Disclaimer */}
          <Alert>
            <Info className="h-4 w-4" />
            <AlertDescription className={language === 'ar' ? 'text-right' : 'text-left'}>
              <strong>{text[language].disclaimer}:</strong> {text[language].disclaimerText}
            </AlertDescription>
          </Alert>

          {/* Image Quality Assessment */}
          {results.imageQuality && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].imageQuality}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className={`flex justify-between items-center ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                    <span>Sharpness</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={results.imageQuality.sharpness} className="w-24" />
                      <span className={getQualityColor(results.imageQuality.sharpness)}>
                        {results.imageQuality.sharpness}%
                      </span>
                    </div>
                  </div>
                  <div className={`flex justify-between items-center ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                    <span>Lighting</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={results.imageQuality.lighting} className="w-24" />
                      <span className={getQualityColor(results.imageQuality.lighting)}>
                        {results.imageQuality.lighting}%
                      </span>
                    </div>
                  </div>
                  <div className={`flex justify-between items-center ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                    <span>Resolution</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={results.imageQuality.resolution} className="w-24" />
                      <span className={getQualityColor(results.imageQuality.resolution)}>
                        {results.imageQuality.resolution}%
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Skin Condition Analysis */}
          {results.skinConditionAnalysis && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].skinCondition}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className={`flex justify-between items-start ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                    <div className={language === 'ar' ? 'text-right' : 'text-left'}>
                      <h4 className="font-semibold text-lg">
                        {results.skinConditionAnalysis.primaryCondition}
                      </h4>
                      <p className="text-gray-600">
                        Severity: {results.skinConditionAnalysis.severity}
                      </p>
                    </div>
                    <Badge className="bg-blue-100 text-blue-800">
                      {text[language].probability}: {Math.round(results.skinConditionAnalysis.probability * 100)}%
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Risk Assessment */}
          {results.riskAssessment && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].riskAssessment}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className={`flex justify-between items-center ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                    <span className="font-medium">{text[language].risk}:</span>
                    <Badge className={getRiskColor(results.riskAssessment.level)}>
                      {results.riskAssessment.level}
                    </Badge>
                  </div>
                  {results.riskAssessment.factors && (
                    <div className={language === 'ar' ? 'text-right' : 'text-left'}>
                      <p className="font-medium mb-2">Factors:</p>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {results.riskAssessment.factors.map((factor, index) => (
                          <li key={index}>• {factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          {results.recommendations && results.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].recommendations}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {results.recommendations.map((rec, index) => (
                    <div key={index} className={`p-3 border rounded-lg ${language === 'ar' ? 'text-right' : 'text-left'}`}>
                      <div className={`flex justify-between items-start mb-2 ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                        <p className="font-medium">{rec.action}</p>
                        <Badge variant="outline" className="ml-2">
                          {rec.priority}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Confidence Score */}
          {results.confidenceScore && (
            <Card>
              <CardContent className="pt-6">
                <div className={`flex justify-between items-center ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                  <span className="font-medium">{text[language].confidence}:</span>
                  <Badge variant="outline">
                    {Math.round(results.confidenceScore * 100)}%
                  </Badge>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}

export default ImageAnalyzer

