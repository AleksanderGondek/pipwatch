export interface Entity {
    readonly id: number;
}

export class Tag implements Entity {
    constructor(public id: number, public name: string) {
    }
}
