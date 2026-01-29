import { Injectable, Logger } from '@nestjs/common';
import { hash, verify } from '@node-rs/argon2';
import { customAlphabet } from 'nanoid';

const nanoid = customAlphabet(
  '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
  32,
);

@Injectable()
export class ApiKeyCryptoService {
  private readonly logger = new Logger(ApiKeyCryptoService.name);

  /**
   * Genera una nueva API Key con formato sk_<32 caracteres aleatorios>
   * Proporciona ~190 bits de entropía
   */
  generateKey(): string {
    const key = `sk_${nanoid()}`;
    this.logger.debug('API Key generated');
    return key;
  }

  /**
   * Hashea una API Key usando Argon2
   * Configuración: memory=19MB, timeCost=2, parallelism=1
   */
  async hashKey(plainKey: string): Promise<string> {
    try {
      // @node-rs/argon2 usa parámetros por defecto OWASP recomendados
      const hashedKey = await hash(plainKey);
      return hashedKey;
    } catch (error) {
      this.logger.error('Failed to hash API Key', error);
      throw error;
    }
  }

  /**
   * Verifica una API Key contra su hash
   * Retorna true si coinciden, false si no
   */
  async verifyKey(plainKey: string, hashedKey: string): Promise<boolean> {
    try {
      const isValid = await verify(hashedKey, plainKey);
      return isValid;
    } catch (error) {
      this.logger.error('Failed to verify API Key', error);
      return false;
    }
  }
}
