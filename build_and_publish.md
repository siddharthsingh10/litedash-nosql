# Building and Publishing PersonalDB to PyPI

## Prerequisites

1. **Install build tools**:
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install build twine
   ```

2. **Create PyPI account** (if you don't have one):
   - Go to https://pypi.org/account/register/
   - Create an account and verify your email

## Building the Package

### 1. Clean previous builds
```bash
rm -rf dist/ build/ *.egg-info/
```

### 2. Build the package
```bash
python3 -m build
```

This creates:
- `dist/personaldb-1.0.0.tar.gz` (source distribution)
- `dist/personaldb-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Check the build
```bash
# List files in the package
tar -tzf dist/personaldb-1.0.0.tar.gz

# Check wheel contents
unzip -l dist/personaldb-1.0.0-py3-none-any.whl
```

## Publishing to PyPI

### 1. Test on TestPyPI first (recommended)
```bash
# Upload to TestPyPI
python3 -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ personaldb
```

### 2. Publish to PyPI
```bash
# Upload to PyPI
python3 -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

### 3. Verify the upload
```bash
# Install from PyPI
python3 -m pip install personaldb

# Test the installation
python3 -c "from personaldb import Database; print('PersonalDB installed successfully!')"
```

## Version Management

### Update version in multiple files:
1. `setup.py` - Update `version="1.0.0"`
2. `personaldb/__init__.py` - Update `__version__ = "1.0.0"`

### Create a new release:
```bash
# Update version numbers
# Build new package
python3 -m build

# Upload to PyPI
python3 -m twine upload dist/*
```

## Package Information

### Package Name: `personaldb`
- **PyPI URL**: https://pypi.org/project/personaldb/
- **GitHub URL**: https://github.com/personaldb/personaldb
- **Documentation**: https://personaldb.readthedocs.io

### Package Features:
- ✅ Lightweight document database
- ✅ MongoDB-like query language
- ✅ Indexing for performance
- ✅ CLI interface
- ✅ Backup/restore functionality
- ✅ Full type hints
- ✅ Comprehensive tests

### Installation:
```bash
pip install personaldb
```

### Usage:
```python
from personaldb import Database

db = Database("my_data")
doc_id = db.insert({"name": "Alice", "age": 25})
users = db.find({"age": {"$gte": 25}})
```

### CLI Usage:
```bash
personaldb create mydb
personaldb insert mydb '{"name": "Alice", "age": 25}'
personaldb find mydb '{"age": {"$gte": 25}}'
```

## Troubleshooting

### Common Issues:

1. **Package name already exists**:
   - Check if `personaldb` is available on PyPI
   - Consider alternative names: `pydocdb`, `lightdocdb`, `simpledb`

2. **Build errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check that `MANIFEST.in` includes all necessary files

3. **Import errors**:
   - Verify package structure is correct
   - Check `__init__.py` exports

4. **CLI not found**:
   - Ensure `entry_points` in `setup.py` is correct
   - Reinstall package: `pip install -e .`

### Testing Before Publishing:

```bash
# Install in development mode
pip install -e .

# Test CLI
python3 -m personaldb.cli --help

# Test Python API
python3 -c "from personaldb import Database; db = Database('test'); print('API works!')"

# Run tests
python3 -m pytest tests/ -v
```

## Post-Publishing Checklist

- [ ] Package is available on PyPI
- [ ] Installation works: `pip install personaldb`
- [ ] CLI works: `personaldb --help`
- [ ] Python API works: `from personaldb import Database`
- [ ] Documentation is updated
- [ ] GitHub repository is updated
- [ ] Release notes are published

## Future Improvements

1. **Documentation**:
   - Set up ReadTheDocs
   - Add more examples
   - Create tutorials

2. **Features**:
   - Add aggregation pipeline
   - Support for transactions
   - Connection pooling
   - Async support

3. **Performance**:
   - Optimize indexing
   - Add compression
   - Implement caching

4. **Testing**:
   - Add integration tests
   - Performance benchmarks
   - Compatibility tests 