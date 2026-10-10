"""
CipherForge - Web Application
Production-ready Flask application for password generation and management.
Easily deployable to Render, Railway, Heroku, or any cloud provider.
"""

import os
import io
import csv
import json
from flask import Flask, render_template, request, jsonify, send_file, Response
from password_generator import PasswordGenerator

app = Flask(__name__)

# Initialize single generator instance with history enabled
generator = PasswordGenerator(enable_history=True)


@app.route('/')
def home():
    """Render main application page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate password(s) with custom parameters"""
    try:
        data = request.get_json() or {}
        
        length = int(data.get('length', 16))
        use_uppercase = bool(data.get('use_uppercase', True))
        use_lowercase = bool(data.get('use_lowercase', True))
        use_digits = bool(data.get('use_digits', True))
        use_symbols = bool(data.get('use_symbols', True))
        exclude_similar = bool(data.get('exclude_similar', False))
        count = max(1, min(int(data.get('count', 1)), 20))  # Between 1 and 20

        passwords = []
        for _ in range(count):
            pwd = generator.generate(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_similar=exclude_similar
            )
            passwords.append(pwd)

        strength_data = generator.check_strength(passwords[0])

        return jsonify({
            'success': True,
            'passwords': passwords,
            'strength': strength_data
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f"Internal error: {str(e)}"}), 500


@app.route('/api/history', methods=['GET'])
def api_history():
    """Fetch recent password generation history"""
    try:
        limit = request.args.get('limit', default=20, type=int)
        history = generator.get_history(limit=limit)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Fetch password generation statistics"""
    try:
        if generator.history:
            stats = generator.history.get_statistics()
        else:
            stats = {
                'total_generated': 0,
                'average_length': 0,
                'most_common_length': 0,
                'strength_distribution': {}
            }
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/clear-history', methods=['POST'])
def api_clear_history():
    """Clear all password generation history"""
    try:
        if generator.history:
            generator.history.clear_history()
        return jsonify({'success': True, 'message': 'History cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export/<file_format>', methods=['GET'])
def api_export(file_format):
    """Export password history as JSON or CSV download"""
    try:
        history = generator.get_history() or []
        
        if file_format.lower() == 'csv':
            output = io.StringIO()
            if history:
                fieldnames = ['password', 'timestamp', 'length', 'strength']
                writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for entry in history:
                    writer.writerow({
                        'password': entry.get('password', ''),
                        'timestamp': entry.get('timestamp', ''),
                        'length': entry.get('length', ''),
                        'strength': entry.get('strength', '')
                    })
            mem = io.BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
            return send_file(
                mem,
                mimetype='text/csv',
                as_attachment=True,
                download_name='password_history.csv'
            )
        else:
            json_str = json.dumps(history, indent=2, ensure_ascii=False)
            mem = io.BytesIO()
            mem.write(json_str.encode('utf-8'))
            mem.seek(0)
            return send_file(
                mem,
                mimetype='application/json',
                as_attachment=True,
                download_name='password_history.json'
            )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    print(f"🚀 CipherForge server running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
