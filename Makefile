.PHONY: clean

clean:
	@echo "Cleaning .next directory..."
	@rm -rf frontend/.next
	@echo "Cleaning .venv directory..."
	@rm -rf backend/.venv
	@echo "Cleaning node_modules..."
	@rm -rf frontend/node_modules
	@echo "Cleaning Python cache..."
	@find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find backend -type f -name "*.pyc" -delete 2>/dev/null || true
	@find backend -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Cleaning system files..."
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "Done!"
