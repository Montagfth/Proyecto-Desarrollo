-- Habilitar el soporte de llaves foráneas en SQLite
PRAGMA foreign_keys = ON;

---
-- 1. TABLA: users
---
CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
);

---
-- 2. TABLA: print_types
---
CREATE TABLE print_types (
  type_id INTEGER PRIMARY KEY AUTOINCREMENT,
  print_type TEXT NOT NULL UNIQUE
);

---
-- 3. TABLA: print_sizes
---
CREATE TABLE print_sizes (
  size_id INTEGER PRIMARY KEY AUTOINCREMENT,
  print_size TEXT NOT NULL UNIQUE
);

---
-- 4. TABLA: print_materials
---
CREATE TABLE print_materials (
  material_id INTEGER PRIMARY KEY AUTOINCREMENT,
  print_material TEXT NOT NULL UNIQUE
);

---
-- 5. TABLA: print_machines
---
CREATE TABLE print_machines (
  machine_id INTEGER PRIMARY KEY AUTOINCREMENT,
  print_machine TEXT NOT NULL UNIQUE
);


---
-- 6. TABLA: orders
---
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  client TEXT,
  print_type INTEGER NOT NULL,
  print_size INTEGER NOT NULL,
  print_material INTEGER NOT NULL,
  print_machine INTEGER NOT NULL,
  colored INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  total INTEGER NOT NULL,
  priority INTEGER DEFAULT 0 CHECK (priority IN (0, 1)),
  created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status TEXT NOT NULL DEFAULT 'Pendiente' CHECK (status IN ('Pendiente', 'Producción', 'Completado')),
  started_at TEXT,
  completed_at TEXT,
  estimated_time INTEGER,
  final_time INTEGER,
  
  FOREIGN KEY (print_type) REFERENCES print_types(type_id),
  FOREIGN KEY (print_size) REFERENCES print_sizes(size_id),
  FOREIGN KEY (print_material) REFERENCES print_materials(material_id),
  FOREIGN KEY (print_machine) REFERENCES print_machines(machine_id)
);

---
-- INSERTS DE DATOS INICIALES
---

INSERT INTO print_types (print_type) VALUES 
('Banner'), 
('Documento'), 
('Flyer'), 
('Plano'), 
('Tarjeta');

INSERT INTO print_sizes (print_size) VALUES 
('A2'), 
('A3'), 
('A4'), 
('Grande');

INSERT INTO print_materials (print_material) VALUES 
('Bond'), 
('Cartulina'), 
('Couche'), 
('Vinil');

INSERT INTO print_machines (print_machine) VALUES 
('M1'), 
('M2'), 
('M3');