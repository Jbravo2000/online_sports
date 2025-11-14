from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'intel2711'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///online_sports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    equipo_favorito = db.Column(db.String(100))

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    deporte = db.Column(db.String(50), nullable=False)
    imagen_url = db.Column(db.String(300))
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    autor = db.Column(db.String(100))

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_local = db.Column(db.String(100), nullable=False)
    equipo_visitante = db.Column(db.String(100), nullable=False)
    deporte = db.Column(db.String(50), nullable=False)
    liga = db.Column(db.String(100))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    resultado_local = db.Column(db.Integer)
    resultado_visitante = db.Column(db.Integer)
    estado = db.Column(db.String(20))  # 'programado', 'en_vivo', 'finalizado'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100))
    imagen_url = db.Column(db.String(300))
    stock = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas
@app.route('/agregar-datos-deportes')
def agregar_datos_deportes():
    """Ruta para agregar datos específicos de deportes"""
    try:
        # Datos de FÚTBOL
        noticias_futbol = [
            Noticia(
                titulo="Messi gana su octavo Balón de Oro",
                contenido="Lionel Messi hace historia al ganar su octavo Balón de Oro tras su espectacular temporada con el PSG y la selección argentina. El astro argentino supera todos los récords en la gala de premios más importante del fútbol mundial.",
                deporte="futbol",
                autor="Carlos Ruiz",
                destacada=True
            ),
            Noticia(
                titulo="El Real Madrid ficha a joven promesa brasileña",
                contenido="El Real Madrid ha anunciado el fichaje de Endrick, la joven promesa brasileña de 17 años. El delantero llegará al club blanco en julio de 2024 por una cifra cercana a los 60 millones de euros.",
                deporte="futbol",
                autor="María González"
            ),
            Noticia(
                titulo="La Premier League bate récord de asistencia",
                contenido="La Premier League inglesa ha batido su récord histórico de asistencia en los estadios esta temporada, con una media de 40,000 espectadores por partido.",
                deporte="futbol",
                autor="David Smith"
            )
        ]

        # Datos de BALONCESTO
        noticias_baloncesto = [
            Noticia(
                titulo="LeBron James supera los 40,000 puntos",
                contenido="LeBron James se convierte en el primer jugador en la historia de la NBA en superar la barrera de los 40,000 puntos en temporada regular. Un hito histórico para el Rey.",
                deporte="baloncesto",
                autor="Ana López",
                destacada=True
            ),
            Noticia(
                titulo="Los Warriors regresan a la final de conferencia",
                contenido="Golden State Warriors elimina a los Lakers y se clasifica para la final de la conferencia Oeste donde se enfrentará a Denver Nuggets.",
                deporte="baloncesto",
                autor="Robert Johnson"
            ),
            Noticia(
                titulo="Wembanyama gana el Rookie del Año",
                contenido="Victor Wembanyama ha sido elegido Rookie del Año de la NBA tras una temporada espectacular con San Antonio Spurs.",
                deporte="baloncesto",
                autor="Susan Lee"
            )
        ]

        # Datos de TENIS
        noticias_tenis = [
            Noticia(
                titulo="Alcaraz gana su primer Abierto de Australia",
                contenido="Carlos Alcaraz gana el Abierto de Australia tras una espectacular final contra Daniil Medvedev. El español demuestra que es el presente y futuro del tenis mundial.",
                deporte="tenis",
                autor="Pedro Martínez",
                destacada=True
            ),
            Noticia(
                titulo="Nadal anuncia su regreso a las canchas",
                contenido="Rafael Nadal confirma su regreso al circuito ATP tras su lesión. El español espera estar listo para la gira de tierra batida.",
                deporte="tenis",
                autor="Elena Torres"
            ),
            Noticia(
                titulo="Nuevo torneo Masters 1000 en Saudi Arabia",
                contenido="La ATP anuncia un nuevo torneo Masters 1000 en Saudi Arabia que se disputará a partir de 2025.",
                deporte="tenis",
                autor="Ahmed Al-Farsi"
            )
        ]

        # Partidos de FÚTBOL
        partidos_futbol = [
            Partido(
                equipo_local="Barcelona",
                equipo_visitante="Real Madrid",
                deporte="futbol",
                liga="La Liga",
                fecha_hora=datetime(2024, 2, 10, 21, 0),
                estado="programado",
                estadio="Camp Nou"
            ),
            Partido(
                equipo_local="Manchester City",
                equipo_visitante="Liverpool",
                deporte="futbol",
                liga="Premier League",
                fecha_hora=datetime(2024, 2, 11, 18, 30),
                estado="programado",
                estadio="Etihad Stadium"
            ),
            Partido(
                equipo_local="Bayern Munich",
                equipo_visitante="Borussia Dortmund",
                deporte="futbol",
                liga="Bundesliga",
                fecha_hora=datetime(2024, 2, 9, 17, 30),
                estado="en_vivo",
                resultado_local=2,
                resultado_visitante=1,
                estadio="Allianz Arena"
            )
        ]

        # Partidos de BALONCESTO
        partidos_baloncesto = [
            Partido(
                equipo_local="Lakers",
                equipo_visitante="Warriors",
                deporte="baloncesto",
                liga="NBA",
                fecha_hora=datetime(2024, 2, 10, 22, 0),
                estado="programado",
                estadio="Crypto.com Arena"
            ),
            Partido(
                equipo_local="Celtics",
                equipo_visitante="Heat",
                deporte="baloncesto",
                liga="NBA",
                fecha_hora=datetime(2024, 2, 11, 19, 0),
                estado="programado",
                estadio="TD Garden"
            ),
            Partido(
                equipo_local="Bulls",
                equipo_visitante="Knicks",
                deporte="baloncesto",
                liga="NBA",
                fecha_hora=datetime(2024, 2, 9, 20, 30),
                estado="finalizado",
                resultado_local=98,
                resultado_visitante=95,
                estadio="United Center"
            )
        ]

        # Partidos de TENIS
        partidos_tenis = [
            Partido(
                equipo_local="Alcaraz",
                equipo_visitante="Djokovic",
                deporte="tenis",
                liga="ATP Tour",
                fecha_hora=datetime(2024, 2, 12, 16, 0),
                estado="programado",
                estadio="Rod Laver Arena"
            ),
            Partido(
                equipo_local="Nadal",
                equipo_visitante="Medvedev",
                deporte="tenis",
                liga="ATP Tour",
                fecha_hora=datetime(2024, 2, 11, 15, 0),
                estado="en_vivo",
                resultado_local=1,
                resultado_visitante=0,
                estadio="Court Philippe-Chatrier"
            ),
            Partido(
                equipo_local="Swiatek",
                equipo_visitante="Sabalenka",
                deporte="tenis",
                liga="WTA Tour",
                fecha_hora=datetime(2024, 2, 10, 14, 0),
                estado="finalizado",
                resultado_local=2,
                resultado_visitante=0,
                estadio="Centre Court"
            )
        ]

        # Agregar todos los datos a la base de datos
        todas_noticias = noticias_futbol + noticias_baloncesto + noticias_tenis
        todos_partidos = partidos_futbol + partidos_baloncesto + partidos_tenis

        for noticia in todas_noticias:
            db.session.add(noticia)

        for partido in todos_partidos:
            db.session.add(partido)

        db.session.commit()

        return """
        <h1>✅ Datos agregados exitosamente</h1>
        <p>Se han agregado:</p>
        <ul>
            <li>📰 9 noticias (3 por deporte)</li>
            <li>⚽ 9 partidos (3 por deporte)</li>
        </ul>
        <a href="/" class="btn btn-primary">Volver al inicio</a>
        <a href="/noticias" class="btn btn-success">Ver noticias</a>
        <a href="/deportes" class="btn btn-info">Ver deportes</a>
        """

    except Exception as e:
        return f"<h1>❌ Error al agregar datos:</h1><p>{str(e)}</p>"
@app.route('/')
def index():
    noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).limit(6).all()
    partidos = Partido.query.filter(Partido.estado.in_(['en_vivo', 'programado'])).order_by(Partido.fecha_hora).limit(5).all()
    productos = Producto.query.limit(4).all()
    return render_template('index.html', noticias=noticias, partidos=partidos, productos=productos)
@app.route('/agregar-noticia', methods=['GET', 'POST'])
@login_required
def agregar_noticia():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            contenido = request.form['contenido']
            deporte = request.form['deporte']
            autor = request.form['autor']
            destacada = 'destacada' in request.form

            nueva_noticia = Noticia(
                titulo=titulo,
                contenido=contenido,
                deporte=deporte,
                autor=autor,
                destacada=destacada
            )

            db.session.add(nueva_noticia)
            db.session.commit()
            flash('Noticia agregada exitosamente!', 'success')
            return redirect(url_for('noticias'))

        except Exception as e:
            flash(f'Error al agregar noticia: {str(e)}', 'error')

    return render_template('agregar_noticia.html')

@app.route('/agregar-partido', methods=['GET', 'POST'])
@login_required
def agregar_partido():
    if request.method == 'POST':
        try:
            equipo_local = request.form['equipo_local']
            equipo_visitante = request.form['equipo_visitante']
            deporte = request.form['deporte']
            liga = request.form['liga']
            fecha = request.form['fecha']
            hora = request.form['hora']
            estado = request.form['estado']

            # Combinar fecha y hora
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

            nuevo_partido = Partido(
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                deporte=deporte,
                liga=liga,
                fecha_hora=fecha_hora,
                estado=estado
            )

            db.session.add(nuevo_partido)
            db.session.commit()
            flash('Partido agregado exitosamente!', 'success')
            return redirect(url_for('deportes'))

        except Exception as e:
            flash(f'Error al agregar partido: {str(e)}', 'error')

    return render_template('agregar_partido.html')
@app.route('/deportes')
def deportes():
    deporte = request.args.get('deporte', '')
    if deporte:
        noticias = Noticia.query.filter_by(deporte=deporte).order_by(Noticia.fecha_publicacion.desc()).all()
        partidos = Partido.query.filter_by(deporte=deporte).order_by(Partido.fecha_hora).all()
    else:
        noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).all()
        partidos = Partido.query.order_by(Partido.fecha_hora).all()
    
    return render_template('deportes.html', noticias=noticias, partidos=partidos, deporte_seleccionado=deporte)

@app.route('/noticias')
def noticias():
    noticias_lista = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).all()
    return render_template('noticias.html', noticias=noticias_lista)
@app.route('/debug-noticias')
def debug_noticias():
    """Ruta para debug - verificar que las noticias existen"""
    try:
        noticias = Noticia.query.all()
        resultado = []
        for noticia in noticias:
            resultado.append({
                'id': noticia.id,
                'titulo': noticia.titulo,
                'deporte': noticia.deporte,
                'contenido_length': len(noticia.contenido)
            })
        return jsonify(resultado)
    except Exception as e:
        return f"Error: {e}"
@app.route('/noticia/<int:noticia_id>')
def noticia_detalle(noticia_id):
    noticia = Noticia.query.get_or_404(noticia_id)
    return render_template('noticia_detalle.html', noticia=noticia)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.query.filter_by(username=username).first()
        if user and user.password == password:  # En producción usar hash!
            login_user(user)
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
        else:
            nuevo_usuario = Usuario(username=username, email=email, password=password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso! Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/api/partidos')
def api_partidos():
    deporte = request.args.get('deporte', '')
    if deporte:
        partidos = Partido.query.filter_by(deporte=deporte).all()
    else:
        partidos = Partido.query.all()
    
    resultado = []
    for partido in partidos:
        resultado.append({
            'id': partido.id,
            'equipo_local': partido.equipo_local,
            'equipo_visitante': partido.equipo_visitante,
            'deporte': partido.deporte,
            'resultado': f"{partido.resultado_local or '-'} - {partido.resultado_visitante or '-'}",
            'estado': partido.estado,
            'fecha_hora': partido.fecha_hora.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify(resultado)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    