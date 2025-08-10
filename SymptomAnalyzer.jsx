import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Send, AlertTriangle, CheckCircle, Info } from 'lucide-react'
import '../App.css'

const SymptomAnalyzer = ({ language }) => {
  const [symptoms, setSymptoms] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const text = {
    en: {
      title: 'Symptom Analysis',
      description: 'Describe your symptoms in detail. Our AI will analyze them and provide insights.',
      placeholder: 'Describe your symptoms here... (e.g., "I have a headache and fever for 2 days")',
      analyze: 'Analyze Symptoms',
      analyzing: 'Analyzing...',
      results: 'Analysis Results',
      symptoms: 'Detected Symptoms',
      diagnoses: 'Potential Conditions',
      recommendations: 'Recommendations',
      redFlags: 'Important Warnings',
      confidence: 'Confidence Score',
      disclaimer: 'Medical Disclaimer',
      disclaimerText: 'This analysis is for informational purposes only and does not replace professional medical advice. Please consult with a healthcare professional for proper diagnosis and treatment.',
      noSymptoms: 'Please describe your symptoms to get an analysis.',
      analysisError: 'Failed to analyze symptoms. Please try again.',
      severity: 'Severity',
      probability: 'Probability'
    },
    ar: {
      title: 'تحليل الأعراض',
      description: 'اوصف أعراضك بالتفصيل. سيقوم الذكاء الاصطناعي بتحليلها وتقديم الرؤى.',
      placeholder: 'اوصف أعراضك هنا... (مثال: "أعاني من صداع وحمى منذ يومين")',
      analyze: 'تحليل الأعراض',
      analyzing: 'جاري التحليل...',
      results: 'نتائج التحليل',
      symptoms: 'الأعراض المكتشفة',
      diagnoses: 'الحالات المحتملة',
      recommendations: 'التوصيات',
      redFlags: 'تحذيرات مهمة',
      confidence: 'درجة الثقة',
      disclaimer: 'إخلاء المسؤولية الطبية',
      disclaimerText: 'هذا التحليل لأغراض إعلامية فقط ولا يحل محل المشورة الطبية المهنية. يرجى استشارة أخصائي رعاية صحية للحصول على التشخيص والعلاج المناسب.',
      noSymptoms: 'يرجى وصف أعراضك للحصول على التحليل.',
      analysisError: 'فشل في تحليل الأعراض. يرجى المحاولة مرة أخرى.',
      severity: 'الشدة',
      probability: 'الاحتمالية'
    }
  }

  const analyzeSymptoms = async () => {
    if (!symptoms.trim()) {
      setError(text[language].noSymptoms)
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setResults(null)

    try {
      // Mock API call - replace with actual backend call
      const response = await fetch('http://localhost:5000/api/analysis/symptoms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add authorization header when implementing auth
        },
        body: JSON.stringify({
          symptoms: symptoms,
          language: language,
          additionalInfo: {}
        })
      })

      if (!response.ok) {
        throw new Error('Analysis failed')
      }

      const data = await response.json()
      
      if (data.success) {
        setResults(data.data)
      } else {
        throw new Error(data.error?.message || 'Analysis failed')
      }
    } catch (err) {
      setError(text[language].analysisError)
      console.error('Analysis error:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'severe': return 'bg-red-100 text-red-800 border-red-200'
      case 'moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'mild': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getProbabilityColor = (probability) => {
    if (probability >= 0.7) return 'bg-red-100 text-red-800'
    if (probability >= 0.5) return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Input Section */}
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
          <Textarea
            placeholder={text[language].placeholder}
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className={`min-h-32 ${language === 'ar' ? 'text-right' : 'text-left'}`}
            dir={language === 'ar' ? 'rtl' : 'ltr'}
          />
          
          {error && (
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button 
            onClick={analyzeSymptoms}
            disabled={isAnalyzing || !symptoms.trim()}
            className="w-full"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                {text[language].analyzing}
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                {text[language].analyze}
              </>
            )}
          </Button>
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

          {/* Red Flags */}
          {results.redFlags && results.redFlags.length > 0 && (
            <Card className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className={`text-red-800 ${language === 'ar' ? 'text-right' : 'text-left'}`}>
                  <AlertTriangle className="inline mr-2 h-5 w-5" />
                  {text[language].redFlags}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {results.redFlags.map((flag, index) => (
                    <Alert key={index} variant="destructive">
                      <AlertDescription className={language === 'ar' ? 'text-right' : 'text-left'}>
                        {flag.condition} - {flag.action}
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Detected Symptoms */}
          {results.extractedSymptoms && results.extractedSymptoms.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].symptoms}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {results.extractedSymptoms.map((symptom, index) => (
                    <Badge 
                      key={index} 
                      variant="outline"
                      className={getSeverityColor(symptom.severity)}
                    >
                      {symptom.symptom.replace('_', ' ')} 
                      {symptom.severity && (
                        <span className="ml-1 text-xs">
                          ({text[language].severity}: {symptom.severity})
                        </span>
                      )}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Potential Diagnoses */}
          {results.potentialDiagnoses && results.potentialDiagnoses.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className={language === 'ar' ? 'text-right' : 'text-left'}>
                  {text[language].diagnoses}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {results.potentialDiagnoses.map((diagnosis, index) => (
                    <div key={index} className="p-4 border rounded-lg">
                      <div className={`flex justify-between items-start mb-2 ${language === 'ar' ? 'flex-row-reverse' : ''}`}>
                        <h4 className="font-semibold text-lg">{diagnosis.condition}</h4>
                        <Badge className={getProbabilityColor(diagnosis.probability)}>
                          {text[language].probability}: {Math.round(diagnosis.probability * 100)}%
                        </Badge>
                      </div>
                      <p className={`text-gray-600 mb-2 ${language === 'ar' ? 'text-right' : 'text-left'}`}>
                        {diagnosis.description}
                      </p>
                      {diagnosis.icd10Code && (
                        <p className="text-sm text-gray-500">
                          ICD-10: {diagnosis.icd10Code}
                        </p>
                      )}
                    </div>
                  ))}
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
                    <div key={index} className={`flex items-start space-x-3 ${language === 'ar' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <div className={language === 'ar' ? 'text-right' : 'text-left'}>
                        <p className="font-medium">{rec.action}</p>
                        {rec.precautions && (
                          <ul className="text-sm text-gray-600 mt-1">
                            {rec.precautions.map((precaution, idx) => (
                              <li key={idx}>• {precaution}</li>
                            ))}
                          </ul>
                        )}
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

export default SymptomAnalyzer

