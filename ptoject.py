import numpy as np
from PIL import Image
import os

# --- Convert Image to Matrix ---
def img_to_matrix(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    return np.array(img)

# --- Convert Matrix to Image ---
def matrix_to_img(matrix, output_path):
    img = Image.fromarray(matrix.astype(np.uint8))
    img.save(output_path)

# --- Confusion (Permutation) ---
def confusion(matrix, key):
    rows, cols = matrix.shape
    size = rows * cols
    permutation = np.argsort((np.arange(size) * key) % size)
    permuted_matrix = matrix.flatten()[permutation].reshape(rows, cols)
    return permuted_matrix

def inverse_confusion(matrix, key):
    rows, cols = matrix.shape
    size = rows * cols
    permutation = np.argsort((np.arange(size) * key) % size)
    inverse_permutation = np.argsort(permutation)
    return matrix.flatten()[inverse_permutation].reshape(rows, cols)

# --- Diffusion (Substitution) ---
def diffusion(matrix, key):
    rows, cols = matrix.shape
    matrix = matrix.astype(np.int16)  # Prevent overflow
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = (matrix[i, j] + (key + i + j) % 256) % 256
    return matrix.astype(np.uint8)

def inverse_diffusion(matrix, key):
    rows, cols = matrix.shape
    matrix = matrix.astype(np.int16)  # Prevent underflow
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = (matrix[i, j] - (key + i + j) % 256) % 256
    return matrix.astype(np.uint8)

# --- Encrypt ---
def encrypt(image_path, encrypted_path, key):
    matrix = img_to_matrix(image_path)
    print("\n🟢 Original Matrix:\n", matrix)

    confused = confusion(matrix, key)
    print("\n🟡 After Confusion:\n", confused)

    diffused = diffusion(confused, key)
    print("\n🔵 After Diffusion (Encrypted Matrix):\n", diffused)

    matrix_to_img(diffused, encrypted_path)

# --- Decrypt ---
def decrypt(encrypted_path, decrypted_path, key):
    matrix = img_to_matrix(encrypted_path)
    print("\n🔵 Encrypted Matrix Loaded:\n", matrix)

    undiffused = inverse_diffusion(matrix, key)
    print("\n🔴 After Inverse Diffusion:\n", undiffused)

    recovered = inverse_confusion(undiffused, key)
    print("\n⚪ Recovered Original Matrix:\n", recovered)

    matrix_to_img(recovered, decrypted_path)

# --- Main Program ---
if __name__ == "__main__":
    image_path = r"E:\Eng Ezz Ali study\Universty\Semester 6\Computer Sec\Project\SECURITY\Picture1.jpg"
    encrypted_path = "E:\\Eng Ezz Ali study\\Universty\\Semester 6\\Computer Sec\\Project\\SECURITY\\lena_encrypted.png"
    decrypted_path = "E:\\Eng Ezz Ali study\\Universty\\Semester 6\\Computer Sec\\Project\\SECURITY\\lena_decrypted.png"
    key = 42  # You can change the key

    # Encrypt
    encrypt(image_path, encrypted_path, key)
    print(f"\n✅ Encrypted image saved as {encrypted_path}")

    # Decrypt
    decrypt(encrypted_path, decrypted_path, key)
    print(f"\n✅ Decrypted image saved as {decrypted_path}")