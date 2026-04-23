import { useMemo, useState } from 'react'

const API_BASE = 'https://presets-l14r.onrender.com'

export default function App() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [uploaded, setUploaded] = useState(null)
  const [processedUrl, setProcessedUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const presets = useMemo(() => ['vintage', 'vivid', 'noir'], [])

  const onFileChange = (event) => {
    const selected = event.target.files?.[0]
    if (!selected) return
    setFile(selected)
    setPreviewUrl(URL.createObjectURL(selected))
    setUploaded(null)
    setProcessedUrl('')
    setError('')
  }

  const uploadImage = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const body = new FormData()
      body.append('image', file)

      const res = await fetch(`${API_BASE}/upload/`, {
        method: 'POST',
        body,
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Upload failed')
      setUploaded(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const applyPreset = async (preset) => {
    if (!uploaded?.id) return
    setLoading(true)
    setError('')
    try {
      const body = new FormData()
      body.append('image_id', uploaded.id)
      body.append('preset', preset)

      const res = await fetch(`${API_BASE}/apply-preset/`, {
        method: 'POST',
        body,
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Processing failed')
      setProcessedUrl(data.processed_url)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      <h1>SnapPresets</h1>

      <input type="file" accept="image/*" onChange={onFileChange} />
      <button onClick={uploadImage} disabled={!file || loading}>
        {loading ? 'Working...' : 'Upload Image'}
      </button>

      {previewUrl && (
        <section>
          <h2>Preview</h2>
          <img src={previewUrl} alt="Preview" className="img" />
        </section>
      )}

      <section>
        <h2>Presets</h2>
        <div className="presets">
          {presets.map((preset) => (
            <button
              key={preset}
              onClick={() => applyPreset(preset)}
              disabled={!uploaded || loading}
            >
              {preset}
            </button>
          ))}
        </div>
      </section>

      {processedUrl && (
        <section>
          <h2>Processed Image</h2>
          <img src={processedUrl} alt="Processed output" className="img" />
        </section>
      )}

      {error && <p className="error">{error}</p>}
    </main>
  )
}
