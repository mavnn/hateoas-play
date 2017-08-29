import { Link } from './link';

export class ApiError {
    error : string;
    error_code : number;
    links : Link [];
}
