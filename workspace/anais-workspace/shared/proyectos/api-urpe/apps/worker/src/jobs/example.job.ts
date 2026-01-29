export class ExampleJob {
  async execute(data: any): Promise<void> {
    console.log('Processing job with data:', data);
    // Job logic here
  }
}
