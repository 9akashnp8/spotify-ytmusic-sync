
type Props = {
    name: string;
    found: boolean,
    liked: boolean,
}

export default function SpotifySong({ name, found, liked }: Props) {
    return (
        <div
            style={{
                display: "flex",
                alignItems: "center"
            }}
        >
            <h3>{name}</h3>
            <div>
                <i>{found ? "✅" : "❌"}</i>
                <i>{liked ? "✅" : "❌"}</i>
            </div>
        </div>
    )
}