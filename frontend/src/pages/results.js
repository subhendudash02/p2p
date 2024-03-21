import axios from 'axios';
import Button from 'react-bootstrap/Button';
import { backend_link } from "@/utils/backend";
import { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';

export default function Results() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get(backend_link + "/energy/result")
            .then((res) => {
                setData(res.data.res); // Set the response data directly to the state
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    const algo_run = () => {
        axios.get(backend_link + "/energy/run")
            .then((res) => {
                alert("Algo Run Successfully");
            })
            .catch((err) => {
                alert("Error");
            });
    }

    return (
        <div>
            <Button onClick={algo_run}>Run Algo</Button>
            <Table striped bordered hover size="sm">
                <tbody>
                    {data.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                                <td key={cellIndex}>{cell}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
}
