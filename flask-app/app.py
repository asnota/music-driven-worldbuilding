from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, url_for
import os
import sys
import time
import psutil
import shutil
import torch
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import threading
import uuid
import scipy.io.wavfile

# Add text2light path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'text2light')))

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_DIR'] = 'generated_panorama_web'
app.config['MUSIC_FOLDER'] = 'generated_music'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_DIR'], exist_ok=True)
os.makedirs(app.config['MUSIC_FOLDER'], exist_ok=True)

# Global variables
music_pipeline = None
generation_status = {}

# HDRI model paths
GLOBAL_SAMPLER_LOGDIR = os.path.join(os.path.dirname(__file__), 'text2light', 'logs', 'global_sampler_clip')
LOCAL_SAMPLER_LOGDIR = os.path.join(os.path.dirname(__file__), 'text2light', 'logs', 'local_sampler')
SRITMO_CKPT = os.path.join(os.path.dirname(__file__), 'text2light', 'logs', 'sritmo.pth')
CLIP_EMB_PATH = os.path.join(os.path.dirname(__file__), 'text2light', 'clip_emb.npy')

def initialize_music_pipeline():
    """Initialize MusicLDM pipeline"""
    global music_pipeline
    try:
        from diffusers import MusicLDMPipeline
        repo_id = "ucsd-reach/musicldm"
        music_pipeline = MusicLDMPipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
        if torch.cuda.is_available():
            music_pipeline = music_pipeline.to("cuda")
        else:
            music_pipeline = music_pipeline.to("cpu")
        print("MusicLDM pipeline initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing music pipeline: {e}")
        return False

def get_dir_size(path):
    """Calculate directory size"""
    total_size = 0
    if os.path.exists(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp) if os.path.exists(fp) else 0
    return total_size / (1024 * 1024)

def validate_hdri_model_paths():
    """Validate HDRI model paths"""
    missing_paths = []
    if not os.path.exists(GLOBAL_SAMPLER_LOGDIR):
        missing_paths.append(f"Global sampler logdir: {GLOBAL_SAMPLER_LOGDIR}")
    if not os.path.exists(LOCAL_SAMPLER_LOGDIR):
        missing_paths.append(f"Local sampler logdir: {LOCAL_SAMPLER_LOGDIR}")
    if not os.path.exists(SRITMO_CKPT):
        missing_paths.append(f"SRiTMO checkpoint: {SRITMO_CKPT}")
    if not os.path.exists(CLIP_EMB_PATH):
        missing_paths.append(f"CLIP embedding: {CLIP_EMB_PATH}")
    return missing_paths

def generate_music_async(task_id, prompt, duration, steps):
    """Generate music asynchronously"""
    global music_pipeline, generation_status
    
    try:
        generation_status[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Generating music...'
        }
        
        audio = music_pipeline(
            prompt, 
            num_inference_steps=steps, 
            audio_length_in_s=duration
        ).audios[0]
        
        filename = f"music_{task_id}.wav"
        filepath = os.path.join(app.config['MUSIC_FOLDER'], filename)
        scipy.io.wavfile.write(filepath, rate=16000, data=audio)
        
        generation_status[task_id] = {
            'status': 'completed',
            'progress': 100,
            'message': 'Music generation completed!',
            'filename': filename,
            'filepath': filepath
        }
        
    except Exception as e:
        generation_status[task_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Generation failed: {str(e)}'
        }

# Main page route
@app.route('/')
def index():
    """Main page"""
    return render_template('main.html')

# HDRI generation page route
@app.route('/hdri')
def hdri_page():
    """HDRI generation page"""
    return render_template('hdri.html')

@app.route('/hdri/generate', methods=['POST'])
def generate_hdri():
    """Handle HDRI generation request"""
    generated_image_urls = []
    error_message = None
    metrics_summary = None
    
    prompt = request.form.get('prompt', '').strip()
    
    if not prompt:
        error_message = "Please enter a text prompt."
    else:
        missing_paths = validate_hdri_model_paths()
        if missing_paths:
            error_message = "Missing required model files:\n" + "\n".join(missing_paths)
        else:
            try:
                from text2light import run_text2light_generation
                
                top_k = int(request.form.get('top_k', 100))
                temperature = float(request.form.get('temperature', 1.0))
                batch_size = int(request.form.get('batch_size', 1))
                sr_factor = int(request.form.get('sr_factor', 4))

                timestamp = int(time.time())
                current_output_dir = os.path.join(app.config['GENERATED_DIR'], f'output_{timestamp}')
                os.makedirs(current_output_dir, exist_ok=True)

                # Monitor metrics
                process = psutil.Process()
                initial_rss = process.memory_info().rss / (1024 * 1024)
                start_time = time.time()

                generated_paths = run_text2light_generation(
                    resume_global_path=GLOBAL_SAMPLER_LOGDIR,
                    resume_local_path=LOCAL_SAMPLER_LOGDIR,
                    sritmo_path=SRITMO_CKPT,
                    sr_factor=sr_factor,
                    output_directory=current_output_dir,
                    clip_db_path=CLIP_EMB_PATH,
                    text_input=prompt,
                    top_k=top_k,
                    temperature=temperature,
                    batch_size_arg=batch_size
                )

                # Calculate metrics
                final_rss = process.memory_info().rss / (1024 * 1024)
                execution_time = time.time() - start_time
                
                metrics_summary = (
                    f"Generation finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Execution time: {execution_time:.2f} seconds\n"
                    f"Memory usage: {initial_rss:.2f} -> {final_rss:.2f} MB\n"
                    f"Memory change: {final_rss - initial_rss:+.2f} MB"
                )

                # Find generated image
                base_filename_ldr = f"hrldr_[{prompt}].png"
                expected_ldr_path = os.path.join(current_output_dir, "ldr", base_filename_ldr)
                
                if os.path.exists(expected_ldr_path):
                    relative_path = os.path.relpath(expected_ldr_path, app.config['GENERATED_DIR'])
                    generated_image_urls.append(url_for('generated_files', filename=relative_path))
                else:
                    error_message = f"Generated image not found: {expected_ldr_path}"

            except Exception as e:
                error_message = f"Error during generation: {e}"

    return render_template('hdri.html',
                         generated_image_urls=generated_image_urls,
                         error_message=error_message,
                         metrics_summary=metrics_summary,
                         form_data=request.form)

# Music generation page route
@app.route('/music')
def music_page():
    """Music generation page"""
    return render_template('music.html')

@app.route('/music/generate', methods=['POST'])
def generate_music():
    """Handle music generation request"""
    global music_pipeline
    
    if music_pipeline is None:
        return jsonify({'error': 'Music model not initialized, please try again later'}), 500
    
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    duration = float(data.get('duration', 10.0))
    steps = int(data.get('steps', 200))
    
    if not prompt:
        return jsonify({'error': 'Please enter a music description'}), 400
    
    if duration < 1 or duration > 30:
        return jsonify({'error': 'Music duration must be between 1-30 seconds'}), 400
    
    if steps < 10 or steps > 500:
        return jsonify({'error': 'Inference steps must be between 10-500'}), 400
    
    task_id = str(uuid.uuid4())
    
    thread = threading.Thread(
        target=generate_music_async, 
        args=(task_id, prompt, duration, steps)
    )
    thread.start()
    
    return jsonify({'task_id': task_id})

@app.route('/music/status/<task_id>')
def get_music_status(task_id):
    """Get music generation status"""
    status = generation_status.get(task_id, {
        'status': 'not_found',
        'message': 'Task not found'
    })
    return jsonify(status)

@app.route('/music/download/<filename>')
def download_music(filename):
    """Download generated music file"""
    filepath = os.path.join(app.config['MUSIC_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

# Static file service
@app.route('/generated_panorama_web/<path:filename>')
def generated_files(filename):
    """Serve generated HDRI files"""
    return send_from_directory(app.config['GENERATED_DIR'], filename)

@app.route('/health')
def health_check():
    """Health check"""
    return {'status': 'ok', 'message': 'Application running normally'}

if __name__ == '__main__':
    print("Initializing application...")
    
    # Initialize music model (optional)
    print("Initializing MusicLDM model...")
    music_initialized = initialize_music_pipeline()
    if music_initialized:
        print("Music model initialized successfully")
    else:
        print("Music model initialization failed, music functionality will be unavailable")
    
    print("Starting Flask application...")
    print("Visit http://localhost:5000 to start using")
    app.run(debug=True, port=5000, host='0.0.0.0')
